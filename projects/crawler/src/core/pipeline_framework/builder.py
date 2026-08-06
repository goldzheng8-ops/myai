from __future__ import annotations

from typing import Generic, Self

from .pipeline import Pipeline
from .stage import PipelineStage
from .step import PipelineStep
from .typing import ContextT


class PipelineBuilder(Generic[ContextT]):
    def __init__(self) -> None:
        self._stages: list[PipelineStage[ContextT]] = []
        self._steps: list[PipelineStep[ContextT]] = []

    @property
    def stages(self) -> tuple[PipelineStage[ContextT], ...]:
        return tuple(self._stages)

    @property
    def steps(self) -> tuple[PipelineStep[ContextT], ...]:
        return tuple(self._steps)

    def add_stage(self, stage: PipelineStage[ContextT]) -> Self:
        self._stages.append(stage)
        return self

    def add(self, stage: PipelineStage[ContextT]) -> Self:
        return self.add_stage(stage)

    def add_step(self, step: PipelineStep[ContextT]) -> Self:
        self._steps.append(step)
        return self

    def insert_stage(self, index: int, stage: PipelineStage[ContextT]) -> Self:
        self._stages.insert(index, stage)
        return self

    def clear(self) -> Self:
        self._stages.clear()
        self._steps.clear()
        return self

    def build(self) -> Pipeline[ContextT]:
        return Pipeline(
            name="default_pipeline",
            stages=tuple(self._stages),
            steps=tuple(self._steps),
        )
