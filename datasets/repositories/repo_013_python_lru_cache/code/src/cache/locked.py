from __future__ import annotations
import threading

from src.cache.lru import LRUCache


class ThreadSafeLRUCache:
    """Lock-guarded wrapper around LRUCache for concurrent access."""

    def __init__(self, capacity: int) -> None:
        self._cache = LRUCache(capacity)
        self._lock = threading.Lock()

    def get(self, key: str):
        with self._lock:
            return self._cache.get(key)

    def put(self, key: str, value) -> None:
        with self._lock:
            self._cache.put(key, value)

    def __len__(self) -> int:
        with self._lock:
            return len(self._cache._store)
