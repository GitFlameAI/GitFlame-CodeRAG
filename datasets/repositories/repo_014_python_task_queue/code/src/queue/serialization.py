from __future__ import annotations
import json


def serialize_task(task: dict) -> str:
    """Encode a task dict as a JSON string for storage or transport."""
    return json.dumps(task, sort_keys=True)


def deserialize_task(data: str) -> dict:
    """Decode a JSON string back into a task dict."""
    task = json.loads(data)
    if "id" not in task:
        raise ValueError("serialized task requires an id")
    return task
