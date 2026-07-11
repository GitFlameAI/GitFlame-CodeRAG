import pytest
from src.fsm.machine import StateMachine


def test_invalid_transition_raises():
    m = StateMachine("draft", {"draft": {"submit": "review"}})
    with pytest.raises(ValueError):
        m.fire("approve")
