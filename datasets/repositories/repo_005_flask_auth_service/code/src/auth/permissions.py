"""Role checks derived from a verified token payload."""


class RoleError(Exception):
    """Raised when a caller lacks the required role."""


def require_role(payload: dict, role: str) -> None:
    """Raise RoleError unless the token payload carries the required role."""
    if payload.get("role") != role:
        raise RoleError(f"requires role={role}")


def is_admin(payload: dict) -> bool:
    return payload.get("role") == "admin"
