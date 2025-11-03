"""Small NLP utilities: keyword extraction and summarization stubs."""

import re


def extract_keywords(text: str, top_k: int = 10):
    """Naive keyword extractor: pick most frequent words excluding stopwords."""
    if not text:
        return []
    text = re.sub(r"[^\w\s]", " ", text).lower()
    tokens = [t for t in text.split() if len(t) > 2]
    stop = set(
        [
            "the",
            "and",
            "for",
            "with",
            "that",
            "this",
            "are",
            "you",
            "your",
            "will",
            "their",
            "have",
        ]
    )
    freq = {}
    for t in tokens:
        if t in stop:
            continue
        freq[t] = freq.get(t, 0) + 1
    items = sorted(freq.items(), key=lambda x: -x[1])[:top_k]
    return [w for w, _ in items]
