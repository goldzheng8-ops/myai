from __future__ import annotations

from collections.abc import Awaitable, Callable
from abc import ABC, abstractmethod
from typing import Generic, Protocol, runtime_checkable

from .typing import ContextT
from .pipeline import Pipeline

@runtime_checkable
class PipelineExecutor(Protocol[ContextT]):
    async def execute(self, context: ContextT) -> ContextT:
        ...


@runtime_checkable
class PipelineProcessor(Protocol[ContextT]):
    async def process(
        self,
        context: ContextT,
        next_step:Callable[[ContextT], Awaitable[ContextT]],
    ) -> ContextT:
        ...


class PipelineExecutorProtocol(
    Generic[ContextT],
    ABC,
):

    @abstractmethod
    async def execute(
        self,
        pipeline: Pipeline[ContextT],
        context: ContextT,
    ) -> ContextT:
        ...