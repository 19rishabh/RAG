import streamlit as st
import requests
import os
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="AskMyDocs",
    page_icon="📚",
    layout="wide"
)

st.title("AskMyDocs❓")
st.markdown("Upload your documents and ask questions about them!")

# --- API Configuration ---
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://backend:8000")  # if using docker

# --- Sidebar ---
with st.sidebar:
    st.header("1. Upload Documents")
    st.markdown("Upload new documents here. This will trigger re-indexing.")
    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True,
        type=['pdf', 'txt', 'docx']
    )

    if st.button("Process Uploaded Files"):
        if uploaded_files:
            with st.spinner("Uploading and indexing... This may take a moment."):
                files_to_upload = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
                try:
                    response = requests.post(f"{FASTAPI_URL}/upload-and-index", files=files_to_upload, timeout=300)
                    response.raise_for_status()
                    st.success(response.json().get("message", "Files processed successfully!"))
                except requests.exceptions.RequestException as e:
                    st.error(f"Error during upload/indexing: {e}")
        else:
            st.warning("Please upload at least one file.")

    st.divider()
    
    # --- LLM Provider Selection ---
    st.header("2. Configure LLM")
    IS_DEPLOYED = os.getenv("DEPLOYED", "false").lower() == "true"
    provider = "gemini"

    if not IS_DEPLOYED:
        provider_options = ["Ollama (Local)", "Gemini (Cloud API)"]
        selected_provider_label = st.radio(
            "Choose your LLM Provider:",
            provider_options,
            help="Ollama runs locally. For Gemini, set your API key in the .env file."
        )
        provider = "ollama" if "Ollama" in selected_provider_label else "gemini"
        st.info(f"Using **{provider.upper()}** for answers.")
    else:
        st.info("Running in deployed mode. Using **Gemini API** for answers.")

# --- Main App Logic ---
with st.form(key='query_form'):
    question = st.text_input(
        "Enter your question:",
        placeholder="e.g., What is the main topic of the documents?"
    )
    submit_button = st.form_submit_button(label='Ask')

if submit_button and question:
    with st.spinner("Searching for the answer..."):
        try:
            start_time = time.time()
            payload = {"q": question, "provider": provider}
            response = requests.post(f"{FASTAPI_URL}/ask", json=payload, timeout=180)
            response.raise_for_status()
            duration = time.time() - start_time
            
            result = response.json()
            
            st.subheader("Answer:")
            st.write(result.get("answer", "No answer found."))
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