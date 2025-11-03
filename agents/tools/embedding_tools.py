"""Embedding tool adapters used by agents."""

from core.embeddings.embedding_service import embed_texts, cosine_similarity
from utils.logger import get_logger

logger = get_logger(__name__)


def embed_text(text: str):
    return embed_texts([text])[0]


def score_similarity(a: str, b: str):
    """Compute a simple similarity score scaled to 0-100."""
    vecs = embed_texts([a, b])
    sim = cosine_similarity(vecs[0], vecs[1])
    # scale cosine (in stub it's arbitrary); clamp between 0-1 then scale
    sim = max(0.0, min(1.0, sim))
    return int(round(sim * 100))
