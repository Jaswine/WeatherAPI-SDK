
from typing_extensions import Any
import time


class Cache:
    def __init__(self, limit=10, ttl_seconds=600):
        self.limit = limit
        self.ttl = ttl_seconds
        self.cache = {}

    def add(self, city_name: str, data: Any):
        if len(self.cache) >= self.limit:
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        self.cache[city_name] = {
            'data': data,
            'timestamp': time.time()
        }

    def get(self, city_name: str):
        entry = self.cache.get(city_name)
        if not entry:
            return None

        if time.time() - entry.get('timestamp') > self.ttl:
            del self.cache[city_name]
            return None

        return entry.get('data')

    def keys(self):
        return self.cache.keys()

    def clear(self):
        return self.cache.clear()


