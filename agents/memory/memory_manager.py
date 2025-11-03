"""Unified memory manager for short-term and long-term memory."""

import json
import os
from collections import deque


class ShortTermMemory:
    def __init__(self, max_len=100):
        self.buffer = deque(maxlen=max_len)

    def add(self, item: str):
        self.buffer.append(item)

    def recall(self, n=10):
        return list(self.buffer)[-n:]


class LongTermMemory:
    def __init__(self, path=None):
        self.path = path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "..", "data", "memory.json"
        )
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.store = json.load(f)
        except Exception:
            self.store = {}

    def get(self, key, default=None):
        return self.store.get(key, default)

    def set(self, key, value):
        self.store[key] = value
        self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.store, f, indent=2)


class MemoryManager:
    def __init__(self):
        self.stm = ShortTermMemory()
        self.ltm = LongTermMemory()

    def add_observation(self, text: str):
        self.stm.add(text)

    def recall_recent(self, n=10):
        return self.stm.recall(n)

    def get_long_term(self, key, default=None):
        return self.ltm.get(key, default)

    def set_long_term(self, key, value):
        self.ltm.set(key, value)
