"""Password reset token flow (in-memory, standalone from login tokens)."""

import secrets

_RESET_TOKENS: dict[str, str] = {}  # token -> username


def request_reset(username: str) -> str:
    token = secrets.token_urlsafe(16)
    _RESET_TOKENS[token] = username
    return token


def consume_reset_token(token: str) -> str | None:
    """Return the username for a reset token and invalidate it."""
    return _RESET_TOKENS.pop(token, None)
