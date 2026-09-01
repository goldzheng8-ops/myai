from dataclasses import dataclass, field
from typing import Any

from .pass_ import PipelinePass
from .pipeline import Pipeline
from .stage import PipelineStage
from .step import PipelineStep


@dataclass(slots=True)
class PipelineRuntime:

    pipeline: Pipeline[Any]

    stage: PipelineStage[Any] | None = None

    step: PipelineStep[Any] | None = None

    pass_: PipelinePass[Any] | None = None

    cancelled: bool = False

    exception: Exception | None = None

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )

    def cancel(self) -> None:
        self.cancelled = True

    @property
    def is_cancelled(self) -> bool:
        return self.cancelled

    def reset(self) -> None:
        self.stage = None
        self.step = None
        self.pass_ = None
        self.cancelled = False
        self.exception = None
        self.metadata.clear()

    @classmethod
    def create(
        cls,
        pipeline: Pipeline[Any],
    ) -> "PipelineRuntime":

        return cls(
            pipeline=pipeline,
        )