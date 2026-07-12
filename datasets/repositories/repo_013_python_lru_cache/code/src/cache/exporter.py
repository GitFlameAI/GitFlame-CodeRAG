from __future__ import annotations
from src.cache.stats import CacheStats


class MetricsExporter:
    """Formats CacheStats for external metrics systems."""

    def __init__(self, name: str) -> None:
        self.name = name

    def export(self, stats: CacheStats) -> dict:
        return {
            f"{self.name}.hits": stats.hits,
            f"{self.name}.misses": stats.misses,
            f"{self.name}.hit_rate": stats.hit_rate(),
        }

    def to_text(self, stats: CacheStats) -> str:
        lines = [f"{key} {value}" for key, value in self.export(stats).items()]
        return "\n".join(lines)
