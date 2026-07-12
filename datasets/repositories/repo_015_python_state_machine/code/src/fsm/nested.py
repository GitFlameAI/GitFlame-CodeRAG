from __future__ import annotations
from src.fsm.machine import StateMachine


class NestedStateMachine:
    """A StateMachine whose states may each own their own sub-machine."""

    def __init__(self, outer: StateMachine) -> None:
        self.outer = outer
        self._children: dict[str, StateMachine] = {}

    def attach(self, state: str, child: StateMachine) -> None:
        self._children[state] = child

    def fire(self, event: str) -> str:
        child = self._children.get(self.outer.state)
        if child is not None and child.can(event):
            return child.fire(event)
        return self.outer.fire(event)
