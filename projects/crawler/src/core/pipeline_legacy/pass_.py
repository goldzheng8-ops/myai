from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic

from .descriptor import PipelineDescriptor
from .typing import ContextT, PipelineNext

if TYPE_CHECKING:
    from .runtime import PipelineRuntime


class PipelinePass(
    PipelineDescriptor,
    Generic[ContextT],
    ABC,
):
    """
    Pipeline middleware.
    """

    @abstractmethod
    async def process(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
        next_step: PipelineNext[ContextT],
    ) -> ContextT:
        ...