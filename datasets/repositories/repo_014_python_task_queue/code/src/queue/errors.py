from __future__ import annotations


class RetryExhaustedError(Exception):
    """Raised when with_retry runs out of attempts.

    The original failure is preserved via `__cause__` so callers can
    still inspect the real traceback instead of a generic exception.
    """

    def __init__(self, attempts: int, last_error: BaseException) -> None:
        super().__init__(f"gave up after {attempts} attempts: {last_error}")
        self.attempts = attempts
        self.last_error = last_error
