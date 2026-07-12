from __future__ import annotations


def to_dot(transitions: dict, graph_name: str = "fsm") -> str:
    """Render a transition table as a Graphviz DOT digraph string."""
    lines = [f"digraph {graph_name} {{"]
    for state, events in transitions.items():
        for event, target in events.items():
            lines.append(f'  "{state}" -> "{target}" [label="{event}"];')
    lines.append("}")
    return "\n".join(lines)
