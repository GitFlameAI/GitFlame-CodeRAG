from __future__ import annotations
from src.queue.broker import Broker


class Worker:
    def __init__(self, broker: Broker) -> None:
        self.broker = broker
        self.processed = 0

    def run_once(self, handler) -> bool:
        task = self.broker.dequeue()
        if task is None:
            return False
        handler(task)
        self.processed += 1
        return True
