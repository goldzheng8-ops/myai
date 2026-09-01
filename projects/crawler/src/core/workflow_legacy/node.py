# core/workflow/node.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic

from core.pipeline_legacy import Pipeline

from .descriptor import WorkflowDescriptor
from .typing import ContextT, NodeId


@dataclass(slots=True)
class WorkflowNode(
    WorkflowDescriptor,
    Generic[ContextT],
):
    """
    A node in a workflow DAG.

    A node represents one executable Pipeline.
    """

    id: NodeId

    pipeline: Pipeline[ContextT]

    terminal: bool = False