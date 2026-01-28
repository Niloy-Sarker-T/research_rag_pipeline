import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict

# Load model once (can swap model name easily)
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
model = SentenceTransformer(EMBEDDING_MODEL)

def embed_chunks_advanced(chunks: List[Dict], batch_size: int = 32) -> List[Dict]:
    """
    Generates embeddings for a list of chunks and returns a list of dicts:
    {
        'chunk_id': int,
        'section': str,
        'page_number': int,
        'text': str,
        'embedding': np.array
    }
    Supports batching for large datasets.
    """
    embeddings = []
    texts = [chunk['text'] for chunk in chunks]

    # Batch encoding
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_emb = model.encode(batch_texts, show_progress_bar=True)
        embeddings.extend(batch_emb)

    # Attach embeddings to chunk metadata
    embedded_chunks = []
    for chunk, emb in zip(chunks, embeddings):
        embedded_chunks.append({
            'chunk_id': chunk['chunk_id'],
            'section': chunk.get('section', 'Unknown'),
            'page_number': chunk.get('page_number', -1),
            'text': chunk['text'],
            'embedding': emb
        })

    return embedded_chunks
