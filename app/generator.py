import os
import requests
import json
import google.generativeai as genai
from typing import List, Dict
from app.config import settings

def compose_prompt(query: str, chunks: List[Dict]) -> str:
    ctx = "\n\n".join(f"[{c.get('source')}] {c.get('text')}" for c in chunks)
    prompt = f"""You are a helpful assistant. Answer the question using ONLY the context below. If the context doesn't contain the answer, say "I don't know." Provide a concise answer and cite sources as [source_file_name.pdf].

Context:
{ctx}

Question: {query}
Answer:"""
    return prompt

def _generate_with_ollama(prompt: str) -> str:
    """Sends a prompt to the Ollama API."""
    url = f"{settings.OLLAMA_URL}/api/generate"
    payload = {"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False}
    try:
        r = requests.post(url, json=payload, timeout=180)
        r.raise_for_status()
        data = r.json()
        return data.get("response") or json.dumps(data)
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama: {e}"

def _generate_with_gemini(prompt: str) -> str:
    """Sends a prompt to the Google Gemini API."""
    api_key = settings.GOOGLE_API_KEY
    if not api_key or api_key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
        return "Error: GOOGLE_API_KEY is not set. Please set it in your .env file or as a deployment secret."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Google Gemini API: {e}"

def generate_answer(prompt: str, provider: str) -> str:
    """
    Main function to generate an answer.
    It calls the appropriate service based on the provided provider.
    """
    provider_lower = provider.lower()
    if provider_lower == "ollama":
        return _generate_with_ollama(prompt)
    elif provider_lower == "gemini":
        return _generate_with_gemini(prompt)
    else:
        return f"Error: Unknown LLM provider '{provider}'. Please choose 'ollama' or 'gemini'."

