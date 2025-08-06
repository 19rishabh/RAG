# Document Q&A System with RAG Framework

This repository implements a **Document Q&A System** using the **Retrieval-Augmented Generation (RAG)** framework. Built with **Streamlit** for the user interface, it allows users to upload PDF documents and ask questions, retrieving answers based on the document content. The system is optimized for performance, accuracy, and efficiency with robust logging and metrics tracking.

## Features
- **PDF Document Upload and Processing**: Efficiently processes and indexes PDF files for querying.
- **RAG Workflow**: Combines semantic chunking, embedding-based retrieval (FAISS), and LLM-powered answering (using ChatOllama).
- **Streamlit UI**: Intuitive interface for uploading documents, querying, and viewing system metrics.
- **Metrics Logging**: Tracks query latency, success rate, and overall performance.
- **Optimized Components**: Uses Hugging Face embeddings, FAISS for vector storage, and lightweight LLMs for inference.

## Built With
- **LangChain**: For chaining prompts and LLMs.
- **Streamlit**: For building the interactive user interface.
- **FAISS**: For efficient vector-based retrieval.
- **Hugging Face Embeddings**: For semantic vectorization.
- **ChatOllama**: For generating answers with LLMs.

## Use Cases
- Research assistants for document-heavy domains.
- Automated Q&A systems for organizational knowledge bases.
- Streamlining document search and analysis workflows.

## How to Run
Follow these steps to set up and run the application:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/19rishabh/RAG.git
   
2. **Navigate to the repository directory**:
```
cd RAG
```

3. **Install dependencies (make sure you have Python installed)**

4. **Run the application**:
```
streamlit run app.py
```

Open the URL displayed in the terminal (typically http://localhost:8501) in your web browser to access the app.
