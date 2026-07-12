from __future__ import annotations
import time

from src.cache.ttl import TTLCache


class TTLSweeper:
    """Proactively purges expired entries from a TTLCache.

    TTLCache only removes expired entries lazily, on the next get().
    A sweeper lets callers reclaim memory from keys that are never
    read again after expiring.
    """

    def __init__(self, cache: TTLCache) -> None:
        self.cache = cache

    def sweep(self) -> int:
        """Remove all expired entries and return how many were purged."""
        now = time.time()
        expired = [
            key
            for key, (expires_at, _value) in self.cache._store.items()
            if expires_at < now
        ]
        for key in expired:
            del self.cache._store[key]
        return len(expired)
