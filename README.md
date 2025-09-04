# 📚 AskMyDocs – Local RAG with Ollama + Huggingface

AskMyDocs is a powerful, self-contained **Retrieval-Augmented Generation (RAG)** application that allows you to chat with your own documents. It runs entirely on your local machine, ensuring your data remains completely private.
It uses:  
- **FastAPI** → Backend for embeddings, FAISS index, and RAG pipeline  
- **Streamlit** → Frontend for uploading docs and chatting with them  
- **Ollama** → Local LLM inference (e.g., Llama 3)  
- **Gemini** → Cloud LLM inference
- **Sentence Transformers** → Powerful Embeddings
- **FAISS** → Vector indexing
- **Docker** → Containerization

## 🚀 Features
 
- **Local & Private**: Your documents and questions never leave your machine. The entire RAG pipeline runs locally and offline.
- **Interactive UI**: A simple and intuitive web interface built with Streamlit for uploading documents and asking questions.
- **Live Document Upload**: Upload your own PDF, DOCX, or TXT files directly through the web interface. The knowledge base is updated on the fly.
- **High-Quality Embeddings**: Uses sentence-transformers to generate state-of-the-art vector embeddings for your documents.
- **Fast Vector Search**: Utilizes FAISS for efficient and fast retrieval of relevant document chunks.
- **Powerful Local LLM**: Powered by Ollama and the Llama 3.1 model by default, providing high-quality answers without an internet connection.
- **Optional Cloud LLM Support**: Easily switch to the powerful Google Gemini API for cloud-based inference, perfect for deployment or lighter local setups.
- **Containerized with Docker**: You can get the applicaton running with a single command.

## 🛠️ Prerequisites
- Docker installed and running    
- At least 8GB free disk space

## ⚙️ Setup & Run  

### 1️⃣ Clone repo
```
git clone https://github.com/19rishabh/RAG.git
cd askmydocs
```
### 2️⃣ Configure .env in root off folder:
```
LLM_PROVIDER="ollama"
GOOGLE_API_KEY="YOUR_KEY"
DEPLOYED="false"
```
### 3️⃣ Build image
The first time you run this command, it will take several minutes.
```
docker compose up --build
```
### 4️⃣ Pull model into Ollama (One-time setup) 
The first time you build the image you need to pull the model manually and restart:
```
docker compose exec ollama ollama pull llama3.1:8b
docker compose restart backend
```
### Now open: http://localhost:8501
