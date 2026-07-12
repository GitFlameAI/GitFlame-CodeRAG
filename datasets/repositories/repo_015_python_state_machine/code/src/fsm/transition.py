from __future__ import annotations
from dataclasses import dataclass, field
import time


@dataclass(frozen=True)
class Transition:
    """A single recorded event + resulting state, with a timestamp."""

    event: str
    state: str
    timestamp: float = field(default_factory=time.time)

    def as_tuple(self) -> tuple[str, str]:
        return (self.event, self.state)
