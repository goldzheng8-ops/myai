from __future__ import annotations

from collections.abc import Sequence
from typing import Generic

from .descriptor import PipelineDescriptor
from .stage import PipelineStage
from .step import PipelineStep
from .typing import ContextT


class Pipeline(PipelineDescriptor, Generic[ContextT]):
    def __init__(
        self,
        name: str | None = None,
        *,
        stages: Sequence[PipelineStage[ContextT]] = (),
        steps: Sequence[PipelineStep[ContextT]] = (),
        description: str = "",
    ) -> None:
        super().__init__(name=name or "pipeline", description=description)
        self._stages = tuple(stages)
        self._steps = tuple(steps)

    @property
    def stages(self) -> tuple[PipelineStage[ContextT], ...]:
        return self._stages

    @property
    def steps(self) -> tuple[PipelineStep[ContextT], ...]:
        return self._steps

    async def execute(self, context: ContextT) -> ContextT:
        current = context
        for stage in self._stages:
            current = await stage.execute(current)
        for step in self._steps:
            current = await step.execute(current)
        return current
