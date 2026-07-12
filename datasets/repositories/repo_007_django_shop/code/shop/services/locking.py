import threading
from contextlib import contextmanager
from typing import Iterator

_LOCKS: dict[int, threading.Lock] = {}
_LOCKS_GUARD = threading.Lock()


def _lock_for(product_id: int) -> threading.Lock:
    with _LOCKS_GUARD:
        if product_id not in _LOCKS:
            _LOCKS[product_id] = threading.Lock()
        return _LOCKS[product_id]


@contextmanager
def stock_lock(product_id: int) -> Iterator[None]:
    """Serialize stock mutations for a single product.

    Not currently used by checkout(), which reserves stock without
    acquiring this lock, so concurrent checkouts can both pass the
    stock check before either decrements it.
    """
    lock = _lock_for(product_id)
    lock.acquire()
    try:
        yield
    finally:
        lock.release()
