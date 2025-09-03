import time
import logging
import json
from app.store_faiss import load_faiss_index
from app.retriever import retrieve
from app.generator import compose_prompt, generate_answer
from app.config import settings
from typing import Optional

perf_logger = logging.getLogger("performance")
perf_logger.setLevel(logging.INFO)

from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler(settings.PERFORMANCE_LOG_PATH, maxBytes=10_000_000, backupCount=5)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_record)

handler.setFormatter(JsonFormatter())
perf_logger.addHandler(handler)


def answer_query(query: str, provider: Optional[str] = None):
    """
    Answers a query by retrieving context and generating a response from the selected LLM provider.
    """
    # --- LLM Provider Logic ---
    if settings.DEPLOYED:
        llm_provider = "gemini"
    elif provider:
        llm_provider = provider
    else:
        llm_provider = settings.LLM_PROVIDER

    start_time = time.time()
    index, metadata = load_faiss_index()
    if index is None or metadata is None:
        return {"error": "Index not ready. Please upload documents and allow time for indexing."}

    chunks = retrieve(index, metadata, query)
    if not chunks:
        ans = "I couldn't find a relevant answer in the documents."
    else:
        prompt = compose_prompt(query, chunks)
        ans = generate_answer(prompt, provider=llm_provider)

    duration = time.time() - start_time
    # Your performance logging logic can remain here
    
    return {"answer": ans, "chunks": chunks}
