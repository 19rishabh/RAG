from app.ingest import load_documents
from app.splitter import docs_to_chunks
from app.embedder import embed_texts
from app.store_faiss import build_faiss_index
from app.config import settings
import os
from pathlib import Path

def build():
    docs = load_documents(settings.DOCS_DIR)
    print(f"Loaded {len(docs)} documents")
    chunks = docs_to_chunks(docs)
    texts = [c["text"] for c in chunks]
    embs = embed_texts(texts)
    print(f"Embeddings shape: {embs.shape if hasattr(embs, 'shape') else 'not array'}")
    # Save metadata (keep full chunk dicts)
    meta = [{"doc_id": c["doc_id"], "text": c["text"], "source": c["source"], "chunk_id": c["chunk_id"]} for c in chunks]
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    idx = build_faiss_index(embs, meta, save_path=settings.FAISS_INDEX_PATH)
    print("Index built. num vectors:", idx.ntotal)

if __name__ == "__main__":
    build()
