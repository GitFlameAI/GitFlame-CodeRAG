from __future__ import annotations
from typing import Callable

from src.cache.lru import LRUCache


class WriteThroughCache:
    """LRUCache that writes every update straight through to a backing store."""

    def __init__(self, capacity: int, writer: Callable[[str, object], None]) -> None:
        self._cache = LRUCache(capacity)
        self._writer = writer

    def get(self, key: str):
        return self._cache.get(key)

    def put(self, key: str, value) -> None:
        self._writer(key, value)
        self._cache.put(key, value)
