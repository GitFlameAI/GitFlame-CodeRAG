"""Optional profile fields for a user, stored apart from credentials."""

_PROFILES: dict[str, dict] = {}


def set_display_name(username: str, display_name: str) -> dict:
    profile = _PROFILES.setdefault(username, {})
    profile["display_name"] = display_name
    return profile


def get_profile(username: str) -> dict:
    return _PROFILES.get(username, {})
