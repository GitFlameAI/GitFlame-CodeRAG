from __future__ import annotations


class Checkpoint:
    """Tracks which row ids have already been processed, for resume support."""

    def __init__(self) -> None:
        self._done: set[int] = set()

    def mark_done(self, row_id: int) -> None:
        self._done.add(row_id)

    def is_done(self, row_id: int) -> bool:
        return row_id in self._done

    def remaining(self, rows: list[dict]) -> list[dict]:
        return [row for row in rows if row["id"] not in self._done]
