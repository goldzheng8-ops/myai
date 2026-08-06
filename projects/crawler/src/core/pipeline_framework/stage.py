from __future__ import annotations

from collections.abc import Sequence

from typing import TYPE_CHECKING, Generic
from core.pipeline_framework.pipeline_pass import PipelinePass
from .descriptor import PipelineDescriptor
from .typing import ContextT

if TYPE_CHECKING:
    from .graph import PipelineGraph




class PipelineStage(PipelineDescriptor, Generic[ContextT]):
    def __init__(
        self,
        name: str | None = None,
        passes: Sequence[PipelinePass[ContextT]] = (),
        *,
        description: str = "",
    ) -> None:
        super().__init__(name=name or self.__class__.__name__, description=description)
        self._passes: list[PipelinePass[ContextT]] = list(passes)

    @property
    def passes(self) -> tuple[PipelinePass[ContextT], ...]:
        return tuple(self._passes)

    def add(self, pass_obj: PipelinePass[ContextT]) -> "PipelineStage[ContextT]":
        self._passes.append(pass_obj)
        return self

    def insert(self, index: int, pass_obj: PipelinePass[ContextT]) -> "PipelineStage[ContextT]":
        self._passes.insert(index, pass_obj)
        return self

    def clear(self) -> None:
        self._passes.clear()

    async def execute(self, context: ContextT) -> ContextT:
        if not self._passes:
            return context

        async def runner(index: int, current: ContextT) -> ContextT:
            if index >= len(self._passes):
                return current
            pass_obj = self._passes[index]
            return await pass_obj.process(current, lambda next_context: runner(index + 1, next_context))

        return await runner(0, context)

    def graph(self) -> "PipelineGraph":
        from .graph import PipelineGraph

        graph = PipelineGraph(name=self.name)
        graph.add_stage(self)
        return graph

    def __iter__(self):
        return iter(self._passes)
