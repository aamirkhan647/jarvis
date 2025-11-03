"""Similarity scorer wraps embeddings and returns a float 0..1."""

from core.embeddings.embedding_service import embed_texts, cosine_similarity


def similarity_score(a: str, b: str) -> float:
    """Return cosine similarity in [0,1]."""
    vecs = embed_texts([a or "", b or ""])
    sim = cosine_similarity(vecs[0], vecs[1])
    # cosine_similarity returns a float; clamp to 0..1
    if sim < 0:
        sim = 0.0
    if sim > 1:
        sim = 1.0
    return float(sim)
