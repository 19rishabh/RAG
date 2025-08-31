import faiss
import numpy as np
import os
from typing import List, Dict
from pathlib import Path
from app.config import settings

def build_faiss_index(embeddings: np.ndarray, metadata: List[Dict], save_path=None):
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)  # inner product on normalized vectors -> cosine
    index.add(embeddings.astype('float32'))
    if save_path:
        faiss.write_index(index, str(save_path))
        np.save(settings.METADATA_PATH, np.array(metadata, dtype=object))
    return index

def load_faiss_index(index_path: str = None):
    index_path = index_path or settings.FAISS_INDEX_PATH
    if not Path(index_path).exists():
        return None, None
    index = faiss.read_index(index_path)
    metadata = np.load(settings.METADATA_PATH, allow_pickle=True)
    return index, list(metadata)

def add_to_index(existing_index, existing_meta, new_embeddings: np.ndarray, new_meta: List[Dict], save_path=None):
    if existing_index is None:
        return build_faiss_index(new_embeddings, new_meta, save_path)
    existing_index.add(new_embeddings.astype('float32'))
    meta = existing_meta + new_meta
    if save_path:
        faiss.write_index(existing_index, str(save_path))
        np.save(settings.METADATA_PATH, np.array(meta, dtype=object))
    return existing_index, meta
