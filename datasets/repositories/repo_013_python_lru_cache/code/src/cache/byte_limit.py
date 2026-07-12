from __future__ import annotations
import sys
from collections import OrderedDict


class ByteLimitedCache:
    """LRU-ordered cache bounded by total value size in bytes rather than count."""

    def __init__(self, max_bytes: int) -> None:
        if max_bytes <= 0:
            raise ValueError("max_bytes must be positive")
        self.max_bytes = max_bytes
        self._store: "OrderedDict[str, object]" = OrderedDict()
        self._used = 0

    def get(self, key: str):
        if key not in self._store:
            return None
        self._store.move_to_end(key)
        return self._store[key]

    def put(self, key: str, value) -> None:
        size = sys.getsizeof(value)
        if key in self._store:
            self._used -= sys.getsizeof(self._store[key])
            self._store.move_to_end(key)
        self._store[key] = value
        self._used += size
        while self._used > self.max_bytes and self._store:
            _, evicted = self._store.popitem(last=False)
            self._used -= sys.getsizeof(evicted)
