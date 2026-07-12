"""In-memory login attempt counter used to throttle brute-force attempts."""

_ATTEMPTS: dict[str, int] = {}
MAX_ATTEMPTS = 5


def record_failure(username: str) -> int:
    _ATTEMPTS[username] = _ATTEMPTS.get(username, 0) + 1
    return _ATTEMPTS[username]


def reset(username: str) -> None:
    _ATTEMPTS.pop(username, None)


def is_locked_out(username: str) -> bool:
    return _ATTEMPTS.get(username, 0) >= MAX_ATTEMPTS
