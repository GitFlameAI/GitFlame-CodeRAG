from __future__ import annotations

from src.cache.lru import LRUCache
from src.cache.stats import CacheStats


class InstrumentedLRUCache:
    """Wraps an LRUCache and records hit/miss counters via CacheStats."""

    def __init__(self, capacity: int) -> None:
        self.cache = LRUCache(capacity)
        self.stats = CacheStats()

    def get(self, key: str):
        value = self.cache.get(key)
        self.stats.record(hit=value is not None)
        return value

    def put(self, key: str, value) -> None:
        self.cache.put(key, value)

    def hit_rate(self) -> float:
        return self.stats.hit_rate()
