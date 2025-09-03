# 📚 AskMyDocs – Local RAG with Ollama + huggingface

AskMyDocs is a **Retrieval-Augmented Generation (RAG) system** that lets you upload your documents (PDFs, text, etc.) and ask natural language questions about them. It uses:  
- **FastAPI** → Backend for embeddings, FAISS index, and RAG pipeline  
- **Streamlit** → Frontend for uploading docs and chatting with them  
- **Ollama** → Local LLM inference (e.g., Llama 3)  

## 🚀 Features
- Supports multiple types (PDF, TXT, DOCX)  
- Recursive Text chunking + embeddings with **sentence-transformers**  
- Vector search via **FAISS**  
- Response generation with **Llama3.1 (via Ollama)**  
- Dockerized setup (backend, frontend, Ollama)  

## 🛠️ Prerequisites
- Docker installed    
- At least **8GB free disk space** 

## ⚙️ Setup & Run  

### 1️⃣ Clone repo
```
git clone https://github.com/<your-username>/askmydocs.git
cd askmydocs
```
### 2️⃣ Configure in .env:
```
LLM_PROVIDER="ollama"
GOOGLE_API_KEY="YOUR_KEY"
DEPLOYED="false"
```
### 3️⃣ Build image
```
docker compose up --build
```

### Now open: http://localhost:8501
