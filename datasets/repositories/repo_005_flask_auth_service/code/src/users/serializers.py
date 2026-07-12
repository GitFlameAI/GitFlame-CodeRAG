"""Serialization helpers that keep sensitive fields out of API responses."""


def public_user(user: dict) -> dict:
    """Return a copy of a user record with secrets like the password stripped."""
    return {"username": user["username"], "role": user.get("role", "member")}


def public_users(users: list[dict]) -> list[dict]:
    return [public_user(u) for u in users]
