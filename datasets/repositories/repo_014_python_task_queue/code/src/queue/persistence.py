from __future__ import annotations
import json
from pathlib import Path

from src.queue.broker import Broker


def save_snapshot(broker: Broker, path: str) -> None:
    """Persist all currently queued tasks to a JSON file."""
    Path(path).write_text(json.dumps(list(broker._queue)))


def load_snapshot(broker: Broker, path: str) -> int:
    """Restore tasks from a snapshot written by save_snapshot().

    Returns the number of tasks re-enqueued.
    """
    data = Path(path)
    if not data.exists():
        return 0
    tasks = json.loads(data.read_text())
    for task in tasks:
        broker.enqueue(task)
    return len(tasks)
