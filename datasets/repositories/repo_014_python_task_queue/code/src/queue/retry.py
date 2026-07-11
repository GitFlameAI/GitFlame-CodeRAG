from __future__ import annotations


def with_retry(func, attempts: int = 3):
    def wrapper(*args, **kwargs):
        last = None
        for _ in range(attempts):
            try:
                return func(*args, **kwargs)
            except Exception as exc:  # noqa: BLE001
                last = exc
        raise last
    return wrapper
