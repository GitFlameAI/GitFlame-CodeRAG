"""Email verification codes (in-memory, standalone demo implementation)."""

import random

_CODES: dict[str, str] = {}


def generate_code(username: str) -> str:
    code = f"{random.randint(0, 999999):06d}"
    _CODES[username] = code
    return code


def verify_code(username: str, code: str) -> bool:
    expected = _CODES.get(username)
    if expected is not None and expected == code:
        del _CODES[username]
        return True
    return False
