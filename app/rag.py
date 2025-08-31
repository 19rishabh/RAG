import time
import logging
import json
from app.store_faiss import load_faiss_index
from app.retriever import retrieve
from app.generator import compose_prompt, generate_answer_ollama
from app.config import settings

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

def answer_query(query: str):
    # 1. Start the timer
    start_time = time.time()
    index, metadata = load_faiss_index()
    if index is None or metadata is None:
        return {"error": "Index not ready. Run indexing first."}
    chunks = retrieve(index, metadata, query)
    if not chunks:
        return {"answer": "I don't know.", "chunks": []}
    prompt = compose_prompt(query, chunks)
    ans = generate_answer_ollama(prompt)
    # 2. Calculate the duration
    duration = time.time() - start_time
    # 3. Log the performance metrics
    perf_logger.info({
        "duration_seconds": round(duration, 2),
        "num_chunks": len(chunks)
    })
    return {"answer": ans, "chunks": chunks}
