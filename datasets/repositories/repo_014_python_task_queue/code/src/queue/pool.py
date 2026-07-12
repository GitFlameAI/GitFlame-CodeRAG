from __future__ import annotations

from src.queue.broker import Broker
from src.queue.worker import Worker


class WorkerPool:
    """Manages a fixed number of Worker instances sharing one Broker."""

    def __init__(self, broker: Broker, size: int) -> None:
        if size <= 0:
            raise ValueError("size must be positive")
        self.workers = [Worker(broker) for _ in range(size)]

    def run_all_once(self, handler) -> int:
        """Let every worker attempt to process one task. Returns tasks processed."""
        processed = 0
        for worker in self.workers:
            if worker.run_once(handler):
                processed += 1
        return processed

    @property
    def total_processed(self) -> int:
        return sum(w.processed for w in self.workers)
