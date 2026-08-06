from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Protocol, runtime_checkable

from .typing import ContextT


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

