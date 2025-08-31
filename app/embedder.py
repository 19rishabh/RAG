from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
from app.config import settings
from pathlib import Path

MODEL = None

def get_model():
    global MODEL
    if MODEL is None:
        MODEL = SentenceTransformer(settings.EMB_MODEL)
    return MODEL

def embed_texts(texts: List[str], batch_size: int = 64) -> np.ndarray:
    model = get_model()
    embs = model.encode(texts, batch_size=batch_size, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)
    return embs
