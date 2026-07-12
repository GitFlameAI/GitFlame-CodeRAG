from __future__ import annotations
from abc import ABC, abstractmethod


class EvictionPolicy(ABC):
    """Strategy for deciding which key to evict next."""

    @abstractmethod
    def touch(self, key: str) -> None:
        """Record that `key` was accessed or inserted."""

    @abstractmethod
    def evict(self) -> str | None:
        """Return the key that should be evicted, if any."""

    @abstractmethod
    def remove(self, key: str) -> None:
        """Stop tracking `key`, e.g. after an explicit delete."""


class NoOpPolicy(EvictionPolicy):
    """Policy for zero-capacity caches: nothing is ever stored or evicted."""

    def touch(self, key: str) -> None:
        return None

    def evict(self) -> str | None:
        return None

    def remove(self, key: str) -> None:
        return None
