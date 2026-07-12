from __future__ import annotations


class DeadLetterQueue:
    """Holds tasks that failed permanently after retries were exhausted."""

    def __init__(self) -> None:
        self._entries: list[tuple[dict, BaseException]] = []

    def add(self, task: dict, error: BaseException) -> None:
        self._entries.append((task, error))

    def __len__(self) -> int:
        return len(self._entries)

    def drain(self) -> list[tuple[dict, BaseException]]:
        """Remove and return all dead-lettered tasks."""
        entries, self._entries = self._entries, []
        return entries
