from __future__ import annotations


class ResultStore:
    """In-memory store mapping task ids to their handler's return value."""

    def __init__(self) -> None:
        self._results: dict[str, object] = {}

    def set(self, task_id: str, result: object) -> None:
        self._results[task_id] = result

    def get(self, task_id: str, default=None):
        return self._results.get(task_id, default)

    def has(self, task_id: str) -> bool:
        return task_id in self._results
