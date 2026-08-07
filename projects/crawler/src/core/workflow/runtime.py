from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from core.runtime.context import RuntimeContext

from .graph import WorkflowGraph
from .typing import NodeId


class NodeExecutionState(
    Enum,
):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class WorkflowRuntime:

    graph: WorkflowGraph[Any]

    context: RuntimeContext

    node_states: dict[
        NodeId,
        NodeExecutionState,
    ] = field(
        default_factory=dict,
    )

    node_errors: dict[
        NodeId,
        Exception,
    ] = field(
        default_factory=dict,
    )

    cancelled: bool = False

    completed: bool = False

    exception: Exception | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    def __post_init__(self) -> None:

        if not self.node_states:

            self.node_states = {
                node_id: NodeExecutionState.PENDING
                for node_id in self.graph.nodes()
            }

    # =========================================================
    # Factory
    # =========================================================

    @classmethod
    def create(
        cls,
        graph: WorkflowGraph[Any],
        context: RuntimeContext,
    ) -> WorkflowRuntime:

        return cls(
            graph=graph,
            context=context,
        )

    # =========================================================
    # Workflow state
    # =========================================================

    @property
    def is_completed(self) -> bool:
        return self.completed

    @property
    def is_cancelled(self) -> bool:
        return self.cancelled

    @property
    def is_failed(self) -> bool:
        return self.exception is not None

    def start(self) -> None:
        self.completed = False
        self.cancelled = False
        self.exception = None

    def complete(self) -> None:
        self.completed = True

    def cancel(self) -> None:
        self.cancelled = True

    def fail(
        self,
        exception: Exception,
    ) -> None:
        self.exception = exception

    # =========================================================
    # Node lifecycle
    # =========================================================

    def start_node(
        self,
        node_id: NodeId,
    ) -> None:

        self.node_states[
            node_id
        ] = NodeExecutionState.RUNNING

    def complete_node(
        self,
        node_id: NodeId,
    ) -> None:

        self.node_states[
            node_id
        ] = NodeExecutionState.COMPLETED

    def fail_node(
        self,
        node_id: NodeId,
        exception: Exception,
    ) -> None:

        self.node_states[
            node_id
        ] = NodeExecutionState.FAILED

        self.node_errors[
            node_id
        ] = exception

    # =========================================================
    # Node queries
    # =========================================================

    def has_completed(
        self,
        node_id: NodeId,
    ) -> bool:

        return (
            self.node_states.get(node_id)
            is NodeExecutionState.COMPLETED
        )

    def is_running(
        self,
        node_id: NodeId,
    ) -> bool:

        return (
            self.node_states.get(node_id)
            is NodeExecutionState.RUNNING
        )

    def is_pending(
        self,
        node_id: NodeId,
    ) -> bool:

        return (
            self.node_states.get(node_id)
            is NodeExecutionState.PENDING
        )

    def is_node_failed(
        self,
        node_id: NodeId,
    ) -> bool:

        return (
            self.node_states.get(node_id)
            is NodeExecutionState.FAILED
        )