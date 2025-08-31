import streamlit as st
import requests
import json
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="AskmyDocs",
    page_icon="📚",
    layout="wide"
)

st.title("AskmyDocs❓")
st.markdown("This app uses a local RAG pipeline to answer questions from your documents.")

# --- API Configuration ---
FASTAPI_URL = "http://localhost:8000/"


# --- Sidebar for Document Upload ---
with st.sidebar:
    st.header("Upload Documents")
    st.markdown("Upload new documents here.")
    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True,
        type=['pdf', 'txt', 'docx']
    )

    if st.button("Process Uploaded Files"):
        if uploaded_files:
            with st.spinner("Uploading and indexing documents... This may take a moment."):
                # Prepare files for multipart/form-data upload
                files_to_upload = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
                try:
                    response = requests.post(f"{FASTAPI_URL}/upload-and-index", files=files_to_upload, timeout=300)
                    response.raise_for_status()
                    st.success(response.json().get("message", "Files processed successfully!"))
                except requests.exceptions.RequestException as e:
                    st.error(f"Error during upload/indexing: {e}")
        else:
            st.warning("Please upload at least one file.")

# --- Main App Logic ---
# Use a form to prevent re-running the app on every keystroke
with st.form(key='query_form'):
    question = st.text_input(
        "Enter your question:",
        placeholder="e.g., What is the main topic of the documents?",
        help="Type your question here and press Enter or click the 'Ask' button."
    )
    submit_button = st.form_submit_button(label='Ask')

if submit_button and question:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching for the answer..."):
            try:
                start_time = time.time()  # Start timer

                # --- Call the FastAPI Backend ---
                payload = {"q": question}
                response = requests.post(f"{FASTAPI_URL}/ask", json=payload, timeout=180)
                response.raise_for_status()  # Raise an exception for bad status codes
                
                end_time = time.time()  # End timer
                duration = end_time - start_time
                
                result = response.json()
                
                # --- Display the Results ---
                st.subheader("Answer:")
                st.write(result.get("answer", "No answer found."))

                # Display the time taken for the query
                st.info(f"Query processed in {duration:.2f} seconds.")

                st.subheader("Sources:")
                if result.get("chunks"):
                    for i, chunk in enumerate(result["chunks"]):
                        with st.expander(f"Source Chunk {i+1} - (Source: {chunk.get('source', 'N/A')})"):
                            st.write(chunk.get("text", "No text available."))
                else:
                    st.write("No source chunks were used for this answer.")

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the backend: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

