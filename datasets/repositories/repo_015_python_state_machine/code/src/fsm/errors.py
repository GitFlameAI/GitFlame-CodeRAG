from __future__ import annotations


class FSMError(Exception):
    """Base class for state machine domain errors."""


class InvalidTransitionError(FSMError):
    """Raised when an event is fired from a state that does not accept it."""

    def __init__(self, event: str, state: str, allowed_events) -> None:
        allowed = ", ".join(sorted(allowed_events)) or "none"
        super().__init__(
            f"invalid transition {event!r} from {state!r}; allowed events: {allowed}"
        )
        self.event = event
        self.state = state
        self.allowed_events = list(allowed_events)


class GuardError(FSMError):
    """Raised by guard checks instead of the built-in PermissionError."""
