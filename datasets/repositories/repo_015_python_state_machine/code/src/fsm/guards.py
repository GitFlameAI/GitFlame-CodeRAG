from __future__ import annotations


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PermissionError(message)


def is_terminal(state: str, terminals: set[str]) -> bool:
    return state in terminals
