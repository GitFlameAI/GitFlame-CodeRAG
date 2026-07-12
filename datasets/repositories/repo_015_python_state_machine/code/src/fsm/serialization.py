from __future__ import annotations
import json

from src.fsm.machine import StateMachine


def to_json(machine: StateMachine) -> str:
    """Serialize a StateMachine's current state and transition table."""
    return json.dumps({"state": machine.state, "transitions": machine.transitions})


def from_json(data: str) -> StateMachine:
    """Rebuild a StateMachine from the output of to_json()."""
    payload = json.loads(data)
    return StateMachine(payload["state"], payload["transitions"])
