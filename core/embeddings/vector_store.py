"""Simple on-disk vector store stub (in-memory dict)."""

import pickle
import os
from typing import Dict, List
from utils.logger import get_logger

logger = get_logger(__name__)


class VectorStore:
    def __init__(self, path=None):
        self.path = path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "..", "data", "vectors.pkl"
        )
        try:
            with open(self.path, "rb") as f:
                self.store = pickle.load(f)
        except Exception:
            self.store = {}

    def upsert(self, key: str, vector):
        self.store[key] = vector
        self._save()

    def query(self, vector, top_k=5):
        # naive euclidean distance ranking
        dists = []
        for k, v in self.store.items():
            try:
                import numpy as np

                d = float(np.linalg.norm(np.array(v) - np.array(vector)))
                dists.append((k, d))
            except Exception:
                continue
        dists.sort(key=lambda x: x[1])
        return [k for k, _ in dists[:top_k]]

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "wb") as f:
            pickle.dump(self.store, f)
        logger.debug("Vector store saved to %s", self.path)
