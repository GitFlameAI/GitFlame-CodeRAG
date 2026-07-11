from __future__ import annotations
import time


class TTLCache:
    """Cache whose entries expire after a time-to-live."""

    def __init__(self, ttl_seconds: float) -> None:
        self.ttl = ttl_seconds
        self._store: dict[str, tuple[float, object]] = {}

    def put(self, key: str, value) -> None:
        self._store[key] = (time.time() + self.ttl, value)

    def get(self, key: str):
        item = self._store.get(key)
        if item is None:
            return None
        expires_at, value = item
        if expires_at < time.time():
            del self._store[key]
            return None
        return value
