from __future__ import annotations
from collections import deque


class Broker:
    """In-memory FIFO task broker."""

    def __init__(self) -> None:
        self._queue: deque = deque()

    def enqueue(self, task: dict) -> None:
        if "id" not in task:
            raise ValueError("task requires an id")
        self._queue.append(task)

    def dequeue(self):
        return self._queue.popleft() if self._queue else None

    def __len__(self) -> int:
        return len(self._queue)
