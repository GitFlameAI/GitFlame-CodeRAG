from __future__ import annotations
import json

from src.cache.lru import LRUCache


def dump(cache: LRUCache) -> str:
    """Serialize an LRUCache's contents to a JSON string, oldest first."""
    return json.dumps(list(cache._store.items()))


def load_into(cache: LRUCache, data: str) -> None:
    """Restore entries from `dump()` output into `cache`, in insertion order."""
    for key, value in json.loads(data):
        cache.put(key, value)


def snapshot(cache: LRUCache) -> dict:
    """Return a plain dict copy of the cache contents without mutating order."""
    return dict(cache._store)
