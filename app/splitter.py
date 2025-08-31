from typing import List, Dict
import re
from app.config import settings

def recursive_character_splitter(text: str, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:

    chunk_size = chunk_size or settings.CHUNK_SIZE
    chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    if len(text) <= chunk_size:
        return [text]

    # 1. Define separators in order of preference for splitting
    separators = ["\\n\\n", "\\n", " ", ""]
    
    # 2. Try to split by the first separator
    final_chunks = []
    current_separator = ""
    for s in separators:
        if s in text:
            splits = text.split(s)
            current_separator = s
            break
    else: # If no separators found, split by character
        splits = list(text)
        current_separator = ""

    # 3. Recursively merge splits into chunks of the desired size
    good_chunks = []
    current_chunk = ""
    for split in splits:
        # If adding the next split doesn't exceed chunk size, add it
        if len(current_chunk) + len(split) + len(current_separator) <= chunk_size:
            current_chunk += split + current_separator
        else:
            # Otherwise, the current chunk is complete
            good_chunks.append(current_chunk.strip())
            # Start a new chunk, respecting the overlap
            current_chunk = current_chunk[-chunk_overlap:] + split + current_separator
    
    # Add the last remaining chunk
    if current_chunk.strip():
        good_chunks.append(current_chunk.strip())
        
    return good_chunks

def docs_to_chunks(docs: List[Dict]) -> List[Dict]:
    """
    Convert a list of documents into chunks using the new splitter.
    """
    out = []
    for d in docs:
        chunks = recursive_character_splitter(d["text"])
        for i, c in enumerate(chunks):
            out.append({
                "doc_id": d["id"],
                "text": c,
                "source": d["source"],
                "chunk_id": f"{d['id']}_{i}"
            })
    return out