from __future__ import annotations

NO_EXPIRY = -1
IMMEDIATE_EXPIRY = 0


def normalize_ttl(ttl_seconds: float) -> float:
    """Clamp a configured TTL to a sane value.

    A ttl of 0 means entries expire immediately rather than living
    forever, and a ttl of -1 is treated as "never expires".
    """
    if ttl_seconds == NO_EXPIRY:
        return float("inf")
    if ttl_seconds < 0:
        raise ValueError("ttl_seconds must be >= -1")
    return ttl_seconds


def is_expired(expires_at: float, now: float) -> bool:
    return expires_at <= now
