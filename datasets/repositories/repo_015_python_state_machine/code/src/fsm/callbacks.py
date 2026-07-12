from __future__ import annotations
from collections import defaultdict
from typing import Callable

Callback = Callable[[str], None]


class CallbackRegistry:
    """Holds on_enter/on_exit callbacks keyed by state name."""

    def __init__(self) -> None:
        self._on_enter: dict[str, list[Callback]] = defaultdict(list)
        self._on_exit: dict[str, list[Callback]] = defaultdict(list)

    def on_enter(self, state: str, callback: Callback) -> None:
        self._on_enter[state].append(callback)

    def on_exit(self, state: str, callback: Callback) -> None:
        self._on_exit[state].append(callback)

    def fire_enter(self, state: str) -> None:
        for callback in self._on_enter[state]:
            callback(state)

    def fire_exit(self, state: str) -> None:
        for callback in self._on_exit[state]:
            callback(state)
