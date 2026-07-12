"""Mutual-exclusion helper to guard non-atomic user operations."""

import threading
from contextlib import contextmanager

_LOCK = threading.Lock()


@contextmanager
def user_write_lock():
    """Serialize check-then-write sequences so concurrent requests cannot race."""
    with _LOCK:
        yield
