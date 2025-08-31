from app.store_faiss import load_faiss_index
from app.retriever import retrieve
from app.generator import compose_prompt, generate_answer_ollama
from app.config import settings

def answer_query(query: str):
    index, metadata = load_faiss_index()
    if index is None or metadata is None:
        return {"error": "Index not ready. Run indexing first."}
    chunks = retrieve(index, metadata, query)
    if not chunks:
        return {"answer": "I don't know.", "chunks": []}
    prompt = compose_prompt(query, chunks)
    ans = generate_answer_ollama(prompt)
    return {"answer": ans, "chunks": chunks}
