from __future__ import annotations


class TransitionBuilder:
    """Fluent helper for building a StateMachine transition table."""

    def __init__(self) -> None:
        self._transitions: dict[str, dict[str, str]] = {}

    def add(self, from_state: str, event: str, to_state: str) -> "TransitionBuilder":
        self._transitions.setdefault(from_state, {})[event] = to_state
        return self

    def build(self) -> dict:
        return self._transitions
