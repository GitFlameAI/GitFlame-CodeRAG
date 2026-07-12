from __future__ import annotations


def validate_transitions(transitions: dict, terminals: set[str]) -> None:
    """Ensure the transition graph is internally consistent.

    Raises ValueError if a terminal state has outgoing transitions, since
    that would let fire() move out of a state meant to be final.
    """
    for state in terminals:
        if transitions.get(state):
            raise ValueError(f"terminal state {state!r} must not have outgoing transitions")


def reachable_states(transitions: dict) -> set[str]:
    """Return every state name referenced anywhere in the transition graph."""
    states = set(transitions.keys())
    for targets in transitions.values():
        states.update(targets.values())
    return states
