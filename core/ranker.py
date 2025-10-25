# core/ranker.py
"""
Ranking module:
- simple TF-IDF based ranking (fast, local)
- placeholder for optional embeddings-based ranking (OpenAI)
"""

import re
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk

logger = logging.getLogger(__name__)
nltk.download("stopwords", quiet=True)
STOPWORDS = set(stopwords.words("english"))


def _clean(text):
    text = re.sub(r"\s+", " ", (text or ""))
    text = re.sub(r"[^\w\s]", " ", text)
    tokens = [
        t.lower() for t in text.split() if t.lower() not in STOPWORDS and len(t) > 1
    ]
    return " ".join(tokens)


def rank_jobs(jobs, resume_text, top_k=50):
    if not jobs:
        return []
    docs = []
    for j in jobs:
        desc = (j.get("description") or "") + " " + (j.get("title") or "")
        docs.append(_clean(desc))
    docs.append(_clean(resume_text or ""))
    try:
        vec = TfidfVectorizer(max_features=4000)
        X = vec.fit_transform(docs)
        resume_v = X[-1]
        job_v = X[:-1]
        sims = cosine_similarity(job_v, resume_v).reshape(-1)
        results = []
        for i, s in enumerate(sims):
            item = jobs[i].copy()
            item["score"] = float(s)
            results.append(item)
        results = sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
        return results
    except Exception as e:
        logger.exception("Ranking failed: %s", e)
        # fallback — return jobs with score 0
        for j in jobs:
            j["score"] = 0.0
        return jobs[:top_k]
