"""Centralized configuration for the auth service."""

import os


def get_secret() -> bytes:
    """Return the token-signing secret from the environment.

    Falls back to a development default; production deployments must set
    AUTH_SECRET_KEY so the secret can be rotated without a code change.
    """
    return os.getenv("AUTH_SECRET_KEY", "change-me").encode()


def get_token_ttl_seconds() -> int:
    return int(os.getenv("AUTH_TOKEN_TTL", "3600"))
