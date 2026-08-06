from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any, Generic

from .descriptor import PipelineDescriptor
from .typing import ContextT


class PipelinePass(PipelineDescriptor, ABC, Generic[ContextT]):
    def __init__(
        self,
        name: str | None = None,
        *,
        description: str = "",
        metadata: dict[str,Any] | None = None,
    ) -> None:
        super().__init__(
            name=name or self.__class__.__name__,
            description=description,
            metadata=metadata or {},
        )

    @abstractmethod
    async def process(
        self,
        context: ContextT,
        next_step: Callable[[ContextT], Awaitable[ContextT]],
    ) -> ContextT:
        ...
