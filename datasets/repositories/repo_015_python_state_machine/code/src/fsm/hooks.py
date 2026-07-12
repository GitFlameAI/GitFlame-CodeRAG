from __future__ import annotations
from typing import Callable

Guard = Callable[[str, str], bool]


class GuardHooks:
    """Registry of guard callbacks run before a transition is allowed."""

    def __init__(self) -> None:
        self._guards: list[Guard] = []

    def add(self, guard: Guard) -> None:
        self._guards.append(guard)

    def check(self, event: str, target_state: str) -> bool:
        """Return True only if every registered guard allows the transition."""
        return all(guard(event, target_state) for guard in self._guards)
