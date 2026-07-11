from __future__ import annotations


class StateMachine:
    """Simple finite state machine."""

    def __init__(self, initial: str, transitions: dict) -> None:
        self.state = initial
        self.transitions = transitions

    def can(self, event: str) -> bool:
        return event in self.transitions.get(self.state, {})

    def fire(self, event: str) -> str:
        if not self.can(event):
            raise ValueError(f"invalid transition {event} from {self.state}")
        self.state = self.transitions[self.state][event]
        return self.state
