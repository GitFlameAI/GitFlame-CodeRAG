from __future__ import annotations


class CacheStats:
    def __init__(self) -> None:
        self.hits = 0
        self.misses = 0

    def record(self, hit: bool) -> None:
        if hit:
            self.hits += 1
        else:
            self.misses += 1

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
