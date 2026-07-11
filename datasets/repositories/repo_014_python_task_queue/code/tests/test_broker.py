import pytest
from src.queue.broker import Broker


def test_enqueue_requires_id():
    with pytest.raises(ValueError):
        Broker().enqueue({})
