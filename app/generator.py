import requests
import json
from typing import List, Dict
from app.config import settings

def compose_prompt(query: str, chunks: List[Dict]) -> str:
    ctx = "\n\n".join(f"[{c.get('doc_id')}] {c.get('text')}" for c in chunks)
    prompt = f"""You are a helpful assistant. Answer the question using ONLY the context below. If the context doesn't contain the answer, say "I don't know." Provide concise answer and cite sources as [doc_id].
Context:
{ctx}
Question: {query}
Answer:"""
    return prompt

def generate_answer_ollama(prompt: str, model: str = None, timeout: int = 180) -> str:
    model = model or settings.OLLAMA_MODEL
    url = f"{settings.OLLAMA_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        return data.get("response") or json.dumps(data)
    except Exception as e:
        return f"Error from Ollama: {e}"
    

