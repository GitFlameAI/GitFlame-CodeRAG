from __future__ import annotations
import time

from src.fsm.machine import StateMachine


class TimeoutTransition:
    """Fires a fallback event if a machine stays in a state too long."""

    def __init__(self, machine: StateMachine, state: str, event: str, after_seconds: float) -> None:
        self.machine = machine
        self.state = state
        self.event = event
        self.after_seconds = after_seconds
        self._entered_at = time.time()

    def reset(self) -> None:
        self._entered_at = time.time()

    def check(self) -> bool:
        """Fire the timeout event if due. Returns True if a transition happened."""
        if self.machine.state != self.state:
            return False
        if time.time() - self._entered_at < self.after_seconds:
            return False
        self.machine.fire(self.event)
        return True
