from __future__ import annotations
from collections import OrderedDict


class LRUCache:
    """Least-recently-used cache with a fixed capacity."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._store: "OrderedDict[str, object]" = OrderedDict()

    def get(self, key: str):
        if key not in self._store:
            return None
        self._store.move_to_end(key)
        return self._store[key]

    def put(self, key: str, value) -> None:
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = value
        if len(self._store) > self.capacity:
            self._store.popitem(last=False)
