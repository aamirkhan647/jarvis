"""A tiny cache manager for job pages and embeddings."""

import time
from collections import OrderedDict


class SimpleCache:
    def __init__(self, max_items=500, ttl=3600):
        self.max_items = max_items
        self.ttl = ttl
        self.data = OrderedDict()

    def set(self, key, value):
        self.data[key] = (time.time(), value)
        if len(self.data) > self.max_items:
            self.data.popitem(last=False)

    def get(self, key, default=None):
        it = self.data.get(key)
        if not it:
            return default
        ts, val = it
        if time.time() - ts > self.ttl:
            del self.data[key]
            return default
        return val
