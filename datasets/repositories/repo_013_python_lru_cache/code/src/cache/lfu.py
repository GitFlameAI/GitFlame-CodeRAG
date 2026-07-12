from __future__ import annotations
from collections import defaultdict


class LFUCache:
    """Least-frequently-used cache with a fixed capacity."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._store: dict[str, object] = {}
        self._freq: dict[str, int] = defaultdict(int)

    def get(self, key: str):
        if key not in self._store:
            return None
        self._freq[key] += 1
        return self._store[key]

    def put(self, key: str, value) -> None:
        if key not in self._store and len(self._store) >= self.capacity:
            evict_key = min(self._freq, key=self._freq.get)
            del self._store[evict_key]
            del self._freq[evict_key]
        self._store[key] = value
        self._freq[key] += 1
