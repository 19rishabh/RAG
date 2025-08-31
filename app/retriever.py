import numpy as np
from typing import List, Dict
from app.embedder import embed_texts
from app.config import settings

def retrieve(index, metadata, query: str, final_k: int = None):
    """
    Retrieves the top k most relevant chunks from the FAISS index 
    """
    # Use final_k directly for the search. TOP_K is no longer needed.
    final_k = final_k or settings.FINAL_K

    # 1. Embed the user's query
    q_emb = embed_texts([query])

    # 2. Search the FAISS index for the top 'final_k' most similar chunks
    # We search directly for the final number of chunks we need.
    distances, indices = index.search(q_emb.astype('float32'), final_k)

    # 3. Get the metadata for the retrieved chunks
    results = []
    for idx in indices[0]:
        # FAISS can return -1 if no chunk is found
        if idx != -1:
            results.append(metadata[idx])
            
    return results

# Please note: removed reranker due to performance issues