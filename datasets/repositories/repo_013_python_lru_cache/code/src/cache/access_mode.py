from __future__ import annotations
from enum import Enum


class AccessMode(Enum):
    """Controls whether get() counts as an access for eviction ordering."""

    TOUCH_ON_GET = "touch_on_get"
    TOUCH_ON_PUT_ONLY = "touch_on_put_only"


DEFAULT_ACCESS_MODE = AccessMode.TOUCH_ON_GET


def should_touch_on_get(mode: AccessMode) -> bool:
    """Return True if a get() should move the key to most-recently-used."""
    return mode is AccessMode.TOUCH_ON_GET


def parse_access_mode(value: str) -> AccessMode:
    """Parse a config string like "touch_on_get" into an AccessMode."""
    for mode in AccessMode:
        if mode.value == value:
            return mode
    raise ValueError(f"unknown access mode: {value!r}")
