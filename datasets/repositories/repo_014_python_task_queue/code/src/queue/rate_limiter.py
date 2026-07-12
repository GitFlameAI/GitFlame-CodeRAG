from __future__ import annotations
import time


class TokenBucketLimiter:
    """Simple token-bucket rate limiter for capping worker throughput."""

    def __init__(self, rate_per_second: float, burst: int) -> None:
        self.rate = rate_per_second
        self.burst = burst
        self._tokens = float(burst)
        self._last = time.time()

    def allow(self) -> bool:
        now = time.time()
        elapsed = now - self._last
        self._last = now
        self._tokens = min(self.burst, self._tokens + elapsed * self.rate)
        if self._tokens >= 1:
            self._tokens -= 1
            return True
        return False
