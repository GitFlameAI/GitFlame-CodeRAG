from gitflame_coderag.schemas import EvidenceChunk, Issue


def build_issue_query(issue: Issue) -> str:
    labels = " ".join(issue.labels)
    return "\n".join(part for part in (issue.title, issue.body, labels) if part).strip()


def retrieve_issue_evidence(issue: Issue, top_k: int) -> list[EvidenceChunk]:
    del issue, top_k
    raise NotImplementedError("full hybrid retrieval is completed in Sprint 2")

