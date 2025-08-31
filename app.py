import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import os
import time
import logging
import csv

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

class OptimizedRAGApp:
    def __init__(self):
        # Initialize components only once
        self.embeddings_model = None
        self.vectorstore = None
        self.retriever = None
        self.llm = None
        self.rag_chain = None
        self.total_queries = 0
        self.successful_queries = 0
        self.total_latency = 0
        self.latency_log_file = "latency_log.csv"

        # Initialize the latency log file
        if not os.path.exists(self.latency_log_file):
            with open(self.latency_log_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Total Queries", "Success Rate (%)", "Average Latency (s)"])

    def load_documents(self, uploaded_files):
        # Reset existing data
        docs = []
        for uploaded_file in uploaded_files:
            try:
                # Save the uploaded file temporarily
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load PDF documents
                loaded_docs = PyPDFLoader(uploaded_file.name).load()
                docs.extend(loaded_docs)
            except Exception as e:
                st.error(f"Error loading {uploaded_file.name}: {str(e)}")
        
        # Initialize embeddings and vectorstore only if documents are loaded
        if docs:
            # Use a faster, smaller embeddings model
            self.embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2")
            
            # Use more efficient text splitting
            text_splitter = SemanticChunker(embeddings=self.embeddings_model)
            
            # Create vectorstore with efficient indexing
            doc_splits = text_splitter.split_documents(docs)
            self.vectorstore = FAISS.from_documents(documents=doc_splits, embedding=self.embeddings_model)
            
            # Configure retriever with fewer documents
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
            
            # Initialize LLM and RAG chain only once
            self.llm = ChatOllama(model="llama3.1", temperature=0)
            
            # Define a more concise prompt template
            prompt = PromptTemplate(
                template="""Answer the question based strictly on the provided context. 
If no relevant information is found, say "I cannot find an answer in the documents."

Question: {question}
Context: {documents}
Answer:""",
                input_variables=["question", "documents"]
            )
            
            # Create the RAG chain
            self.rag_chain = prompt | self.llm | StrOutputParser()
            
            return True
        return False

    def process_query(self, question):
        if not self.retriever or not self.rag_chain:
            return "Please load documents first."

        self.total_queries += 1
        start_time = time.time()

        try:
            # Retrieve relevant documents
            documents = self.retriever.invoke(question)
            if not documents:
                return "No relevant documents found."
            
            # Extract content from retrieved documents
            doc_texts = "\n".join([doc.page_content for doc in documents])

            # Get the answer from the language model
            answer = self.rag_chain.invoke({"question": question, "documents": doc_texts})

            # Calculate latency
            latency = time.time() - start_time
            self.total_latency += latency
            self.successful_queries += 1

            # Log metrics
            avg_latency = self.total_latency / self.total_queries
            success_rate = (self.successful_queries / self.total_queries) * 100
            
            with open(self.latency_log_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    time.strftime("%Y-%m-%d %H:%M:%S"), 
                    self.total_queries, 
                    f"{success_rate:.2f}", 
                    f"{avg_latency:.2f}"
                ])

            return answer
        
        except Exception as e:
            return f"Error processing query: {str(e)}"

    def get_metrics(self):
        if self.total_queries == 0:
            return "No queries processed yet."
        
        avg_latency = self.total_latency / self.total_queries
        success_rate = (self.successful_queries / self.total_queries) * 100
        return f"Queries: {self.total_queries}, Success: {success_rate:.2f}%, Avg Latency: {avg_latency:.2f}s"

# Streamlit app setup
def main():
    st.title("📚 Document Q&A System")
    
    # Initialize RAG app in session state
    if 'rag_app' not in st.session_state:
        st.session_state.rag_app = OptimizedRAGApp()

    # Document upload
    uploaded_files = st.sidebar.file_uploader(
        "Upload PDF documents", type=["pdf"], accept_multiple_files=True
    )

    if uploaded_files:
        with st.spinner("Processing documents..."):
            success = st.session_state.rag_app.load_documents(uploaded_files)
        
        if success:
            st.sidebar.success(f"{len(uploaded_files)} documents loaded.")
        else:
            st.sidebar.error("Failed to load documents.")

    # Query interface
    question = st.text_input("❓Ask a question:")
    
    if st.button("Get Answer"):
        if question.strip():
            with st.spinner("Searching for answer..."):
                answer = st.session_state.rag_app.process_query(question)
            st.write(f"**Answer:** {answer}")
        else:
            st.warning("Please enter a valid question.")

    # Metrics display
    st.sidebar.subheader("Performance Metrics")
    if st.sidebar.button("Show Metrics"):
        metrics = st.session_state.rag_app.get_metrics()
        st.sidebar.write(metrics)

if __name__ == "__main__":
    main()
