from __future__ import annotations

from abc import ABC, abstractmethod

from core.runtime.errors import ContextMergeConflictError

from .context import RuntimeContext


class ContextMergeStrategy(ABC):
    """
    Defines how one RuntimeContext is merged
    into another RuntimeContext.
    """

    @abstractmethod
    def merge(
        self,
        target: RuntimeContext,
        source: RuntimeContext,
    ) -> None:
        ...

class OverwriteContextMergeStrategy(
    ContextMergeStrategy,
):
    """
    Merge source values into target.

    Existing values are overwritten by source values.
    """

    def merge(
        self,
        target: RuntimeContext,
        source: RuntimeContext,
    ) -> None:

        target.merge(source)

class StrictContextMergeStrategy(
    ContextMergeStrategy,
):
    """
    Reject conflicting values during merge.
    """

    def merge(
        self,
        target: RuntimeContext,
        source: RuntimeContext,
    ) -> None:

        target_values = target.as_mapping()
        source_values = source.as_mapping()

        conflicts = tuple(
            key
            for key, value in source_values.items()
            if (
                key in target_values
                and target_values[key] != value
            )
        )

        if conflicts:
            raise ContextMergeConflictError(
                conflicts
            )

        target.merge(source)