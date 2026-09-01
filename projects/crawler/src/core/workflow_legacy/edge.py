# core/workflow/edge.py

from __future__ import annotations

from dataclasses import dataclass

from .typing import NodeId


@dataclass(frozen=True, slots=True)
class WorkflowEdge:
    """
    Directed edge between two workflow nodes.
    """

    source: NodeId

    target: NodeId

    name: str | None = None