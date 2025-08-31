import os
from pydantic_settings import BaseSettings
from pathlib import Path
import yaml

BASE = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DATA_DIR: str = str(BASE / "data")
    DOCS_DIR: str = str(BASE / "docs")
    EMB_MODEL: str = "sentence-transformers/all-MiniLM-L12-v2"
    CHUNK_SIZE: int = 700
    CHUNK_OVERLAP: int = 100
    TOP_K: int = 7
    FINAL_K: int = 5
    FAISS_INDEX_PATH: str = str(BASE / "data" / "faiss.index")
    METADATA_PATH: str = str(BASE / "data" / "metadata.npy")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")  # if using HTTP
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = BASE / ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
