from __future__ import annotations
import uuid


def build_task(payload: dict, task_id: str | None = None) -> dict:
    """Create a well-formed task dict ready for Broker.enqueue()."""
    return {"id": task_id or str(uuid.uuid4()), "payload": payload}


def build_batch(payloads: list[dict]) -> list[dict]:
    """Build a batch of tasks from a list of payloads."""
    return [build_task(payload) for payload in payloads]
