from __future__ import annotations


class History:
    def __init__(self) -> None:
        self.events: list[tuple[str, str]] = []

    def record(self, event: str, state: str) -> None:
        self.events.append((event, state))

    def last_state(self) -> str | None:
        return self.events[-1][1] if self.events else None
