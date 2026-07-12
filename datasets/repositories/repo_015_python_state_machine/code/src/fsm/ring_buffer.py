from __future__ import annotations
from collections import deque


class RingBuffer:
    """Fixed-capacity FIFO buffer that drops the oldest item when full.

    Intended for use by History to keep memory bounded instead of
    growing the event list forever.
    """

    def __init__(self, maxlen: int) -> None:
        if maxlen <= 0:
            raise ValueError("maxlen must be positive")
        self._items: deque = deque(maxlen=maxlen)

    def append(self, item) -> None:
        self._items.append(item)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)
