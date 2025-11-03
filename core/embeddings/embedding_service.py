# """Embedding service stub. Replace with sentence-transformers or provider API."""

# from typing import List
# import numpy as np
# from utils.logger import get_logger

# logger = get_logger(__name__)


# def embed_texts(texts: List[str]) -> List[np.ndarray]:
#     """Return naive vector representations (length = 1) for stubs."""
#     logger.debug("embed_texts called with %d items", len(texts))
#     # For now, produce length-1 numeric vectors based on hash to maintain deterministic behavior
#     vectors = []
#     for t in texts:
#         vectors.append(np.array([float(abs(hash(t)) % 1000)]))
#     return vectors


# def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
#     """Compute cosine between 1-D arrays safely (for stub)."""
#     if a.size == 0 or b.size == 0:
#         return 0.0
#     denom = np.linalg.norm(a) * np.linalg.norm(b)
#     if denom == 0:
#         return 0.0
#     return float(np.dot(a, b) / denom)


"""Embedding service using SentenceTransformers."""

import numpy as np
from sentence_transformers import SentenceTransformer
from utils.logger import get_logger

logger = get_logger(__name__)

_model = None


def _get_model():
    global _model
    if _model is None:
        logger.info("Loading SentenceTransformer model (all-MiniLM-L6-v2)...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts):
    """Embed a list of texts -> list of float vectors."""
    if not texts:
        return []
    model = _get_model()
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings.tolist()


def cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a)
    b = np.array(vec_b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)
