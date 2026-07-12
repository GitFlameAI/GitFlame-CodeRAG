from __future__ import annotations
import heapq
import itertools


class PriorityBroker:
    """FIFO-within-priority task broker backed by a binary heap."""

    def __init__(self) -> None:
        self._heap: list = []
        self._counter = itertools.count()

    def enqueue(self, task: dict, priority: int = 0) -> None:
        if "id" not in task:
            raise ValueError("task requires an id")
        heapq.heappush(self._heap, (priority, next(self._counter), task))

    def dequeue(self):
        if not self._heap:
            return None
        _, _, task = heapq.heappop(self._heap)
        return task

    def __len__(self) -> int:
        return len(self._heap)
