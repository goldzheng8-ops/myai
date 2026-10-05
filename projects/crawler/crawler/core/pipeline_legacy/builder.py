from __future__ import annotations
from typing import Any

from .pipeline import Pipeline
from .stage import PipelineStage
from .step import PipelineStep
from .pass_ import PipelinePass
from .typing import ContextT


class PipelineBuilder:

    def __init__(
        self,
        name: str,
        *,
        description: str = "",
    ) -> None:

        self._pipeline = Pipeline(
            name=name,
            description=description,
        )

        self._current_stage: PipelineStage[Any] | None = None
        self._current_step: PipelineStep[Any] | None = None

    @property
    def pipeline(self) -> Pipeline[Any]:

        return self._pipeline

    def stage(
        self,
        name: str,
        *,
        description: str = "",
    ) -> "PipelineBuilder":

        stage = PipelineStage(
            name=name,
            description=description,
        )

        self._pipeline.add_stage(stage)

        self._current_stage = stage
        self._current_step = None

        return self

    def step(
        self,
        name: str,
        *,
        description: str = "",
    ) -> "PipelineBuilder":

        if self._current_stage is None:
            raise RuntimeError(
                "stage() must be called first."
            )

        step = PipelineStep[Any](
            name=name,
            description=description,
        )

        self._current_stage.add_step(step)

        self._current_step = step

        return self

    def pass_(
        self,
        value: PipelinePass[Any],
    ) -> "PipelineBuilder":

        if self._current_step is None:
            raise RuntimeError(
                "step() must be called first."
            )

        self._current_step.add_pass(value)

        return self

    def passes(
        self,
        *values: PipelinePass[Any],
    ) -> "PipelineBuilder":

        for value in values:
            self.pass_(value)

        return self

    def build(
        self,
    ) -> Pipeline[Any]:

        return self._pipeline.copy()

    def add_stage(
        self,
        stage: PipelineStage[Any],
    ) -> "PipelineBuilder":

        self._pipeline.add_stage(stage)

        self._current_stage = stage
        self._current_step = None

        return self

    def add_step(
        self,
        step: PipelineStep[Any],
    ) -> "PipelineBuilder":

        if self._current_stage is None:
            raise RuntimeError(
                "No current stage."
            )

        self._current_stage.add_step(step)

        self._current_step = step

        return self

    def reset(
        self,
    ) -> "PipelineBuilder":

        self._pipeline.clear()

        self._current_stage = None
        self._current_step = None

        return self

    @classmethod
    def from_pipeline(
        cls,
        pipeline: Pipeline[ContextT],
    ) -> "PipelineBuilder":
        """Create a builder initialized from an existing Pipeline."""
        builder = cls(pipeline.name, description=pipeline.description)
        builder._pipeline = pipeline.copy()
        return builder

'''
from_config(config)
from_yaml(data)
from_json(data)
'''