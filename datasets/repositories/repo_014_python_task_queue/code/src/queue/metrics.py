from __future__ import annotations


class WorkerMetrics:
    """Tracks processed and failed task counts for a Worker."""

    def __init__(self) -> None:
        self.processed = 0
        self.failed = 0

    def record_success(self) -> None:
        self.processed += 1

    def record_failure(self) -> None:
        self.failed += 1

    def snapshot(self) -> dict:
        return {"processed": self.processed, "failed": self.failed}
