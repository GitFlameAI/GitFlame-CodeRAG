from __future__ import annotations
from dataclasses import dataclass


@dataclass
class RowError:
    """Describes a single row that failed to parse or validate."""
    index: int
    reason: str
    raw: dict


class RowErrorCollector:
    """Collects row-level errors so a run can continue past bad rows."""

    def __init__(self) -> None:
        self.errors: list[RowError] = []

    def add(self, index: int, reason: str, raw: dict) -> None:
        self.errors.append(RowError(index=index, reason=reason, raw=raw))

    def has_errors(self) -> bool:
        return bool(self.errors)

    def summary(self) -> str:
        return f"{len(self.errors)} row(s) failed"
