"""Public user profile lookups."""

from app.db import session


def get_profile(username: str) -> dict | None:
    with session() as db:
        user = db.users.get(username)
        if user is None:
            return None
        return {"username": user["username"], "email": user.get("email", "")}


def update_bio(username: str, bio: str) -> dict | None:
    with session() as db:
        user = db.users.get(username)
        if user is None:
            return None
        user["bio"] = bio
        return {"username": username, "bio": bio}
