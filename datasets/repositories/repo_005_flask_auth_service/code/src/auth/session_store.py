"""Refresh-token session store, separate from the short-lived access tokens."""

import secrets

_SESSIONS: dict[str, str] = {}  # refresh token -> username


def issue_refresh_token(username: str) -> str:
    token = secrets.token_urlsafe(24)
    _SESSIONS[token] = username
    return token


def revoke(token: str) -> None:
    _SESSIONS.pop(token, None)


def username_for(token: str) -> str | None:
    return _SESSIONS.get(token)
