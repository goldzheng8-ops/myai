from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from core.runtime.context import RuntimeContext
from core.runtime.merge import (
    ContextMergeStrategy,
    OverwriteContextMergeStrategy,
)

from .typing import NodeId


class WorkflowMergePolicy(ABC):
    """
    Defines how workflow branch contexts
    are merged after a workflow level completes.
    """

    @abstractmethod
    def merge(
        self,
        target: RuntimeContext,
        results: Sequence[
            tuple[NodeId, RuntimeContext]
        ],
    ) -> None:
        ...

class DefaultWorkflowMergePolicy(
    WorkflowMergePolicy,
):

    def __init__(
        self,
        strategy: ContextMergeStrategy | None = None,
    ) -> None:

        self._strategy = (
            strategy
            or OverwriteContextMergeStrategy()
        )

    @property
    def strategy(
        self,
    ) -> ContextMergeStrategy:

        return self._strategy

    def merge(
        self,
        target: RuntimeContext,
        results: Sequence[
            tuple[NodeId, RuntimeContext]
        ],
    ) -> None:

        for _, context in results:

            self._strategy.merge(
                target,
                context,
            )

'''
FirstSuccessWorkflowMergePolicy
PriorityWorkflowMergePolicy
CollectWorkflowMergePolicy
'''