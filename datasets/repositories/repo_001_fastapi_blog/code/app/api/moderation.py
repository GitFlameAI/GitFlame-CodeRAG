"""Reporting posts/comments for moderator review (in-memory)."""

_REPORTS: list[dict] = []


def report_content(content_type: str, content_id: int, reason: str, reporter: str) -> dict:
    report = {
        "id": len(_REPORTS) + 1,
        "type": content_type,
        "content_id": content_id,
        "reason": reason,
        "reporter": reporter,
    }
    _REPORTS.append(report)
    return report


def list_reports() -> list[dict]:
    return list(_REPORTS)
