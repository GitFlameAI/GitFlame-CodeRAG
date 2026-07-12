from __future__ import annotations
from dataclasses import dataclass


@dataclass
class RunMetrics:
    """Per-stage row counts for a single pipeline run."""
    extracted: int = 0
    transformed: int = 0
    unique: int = 0
    loaded: int = 0

    def as_dict(self) -> dict:
        return {
            "extracted": self.extracted,
            "transformed": self.transformed,
            "unique": self.unique,
            "loaded": self.loaded,
        }
