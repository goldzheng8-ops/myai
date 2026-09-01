# core/workflow/errors.py
from .typing import NodeId

class WorkflowError(
    RuntimeError,
):
    """
    Base exception for workflow errors.
    """

class WorkflowGraphError(
    WorkflowError,
):
    """Base exception for workflow graph errors."""


class WorkflowValidationError(
    WorkflowGraphError,
):
    """Workflow graph is invalid."""


class WorkflowCycleError(
    WorkflowValidationError,
):
    """Workflow contains a cycle."""


class WorkflowGraphStaleError(
    WorkflowGraphError,
):
    """Workflow graph snapshot is stale."""


class WorkflowGraphFrozenError(
    WorkflowGraphError,
):
    """Frozen workflow graph cannot be modified."""





class WorkflowExecutionError(
    WorkflowError,
):
    """
    Raised when workflow execution fails.
    """

    def __init__(
        self,
        message: str,
        *,
        node_id: NodeId | None = None,
        cause: Exception | None = None,
    ) -> None:

        self.node_id = node_id
        self.cause = cause

        super().__init__(message)


class WorkflowNodeExecutionError(
    WorkflowExecutionError,
):
    """
    Raised when an individual workflow node fails.
    """

    def __init__(
        self,
        node_id: NodeId,
        cause: Exception,
    ) -> None:

        self.node_id = node_id
        self.cause = cause

        super().__init__(
            "Workflow node execution failed: "
            f"{node_id!r}",
            node_id=node_id,
            cause=cause,
        )


class WorkflowMergeError(
    WorkflowExecutionError,
):
    """
    Raised when workflow branch contexts cannot
    be merged.
    """


class WorkflowCancelledError(
    WorkflowError,
):
    """
    Raised when workflow execution is cancelled.
    """