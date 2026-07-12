from __future__ import annotations
from collections import deque

from src.fsm.machine import StateMachine


class EventQueue:
    """Buffers events to be applied to a StateMachine one at a time."""

    def __init__(self, machine: StateMachine) -> None:
        self.machine = machine
        self._pending: deque = deque()

    def push(self, event: str) -> None:
        self._pending.append(event)

    def process_one(self) -> str | None:
        if not self._pending:
            return None
        event = self._pending.popleft()
        return self.machine.fire(event)

    def process_all(self) -> list[str]:
        results = []
        while self._pending:
            results.append(self.process_one())
        return results
