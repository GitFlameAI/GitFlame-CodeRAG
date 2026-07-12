from __future__ import annotations
import time

from src.queue.broker import Broker


class DelayedScheduler:
    """Holds tasks until their scheduled run time, then releases them to a Broker."""

    def __init__(self, broker: Broker) -> None:
        self.broker = broker
        self._pending: list[tuple[float, dict]] = []

    def schedule(self, task: dict, delay_seconds: float) -> None:
        run_at = time.time() + delay_seconds
        self._pending.append((run_at, task))

    def tick(self) -> int:
        """Enqueue any tasks whose delay has elapsed. Returns how many were released."""
        now = time.time()
        ready = [item for item in self._pending if item[0] <= now]
        self._pending = [item for item in self._pending if item[0] > now]
        for _, task in ready:
            self.broker.enqueue(task)
        return len(ready)
