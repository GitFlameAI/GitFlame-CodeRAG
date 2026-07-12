"""Append-only audit trail for account-related events."""

import time

_EVENTS: list[dict] = []


def record_event(username: str, action: str) -> dict:
    event = {"username": username, "action": action, "at": time.time()}
    _EVENTS.append(event)
    return event


def events_for_user(username: str) -> list[dict]:
    return [e for e in _EVENTS if e["username"] == username]
