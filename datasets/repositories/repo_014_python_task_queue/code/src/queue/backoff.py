from __future__ import annotations


class ExponentialBackoff:
    """Tracks an increasing sleep interval for a worker polling an empty queue."""

    def __init__(self, base: float = 0.1, factor: float = 2.0, max_delay: float = 5.0) -> None:
        self.base = base
        self.factor = factor
        self.max_delay = max_delay
        self._delay = base

    def next_delay(self) -> float:
        delay = self._delay
        self._delay = min(self._delay * self.factor, self.max_delay)
        return delay

    def reset(self) -> None:
        self._delay = self.base
