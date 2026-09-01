from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import Generic

from .descriptor import PipelineDescriptor
from .stage import PipelineStage
from .typing import ContextT


@dataclass(slots=True)
class Pipeline(
    PipelineDescriptor,
    Generic[ContextT],
):

    _stages: list[
        PipelineStage[ContextT]
    ] = field(
        default_factory=list,
    )

    @property
    def stages(
        self,
    ) -> tuple[
        PipelineStage[ContextT],
        ...
    ]:

        return tuple(self._stages)

    def contains(
        self,
        value: PipelineStage[ContextT],
    ) -> bool:

        return value in self._stages

    def add_stage(
        self,
        stage: PipelineStage[ContextT],
    ) -> None:

        self._stages.append(stage)

    def extend(
        self,
        stages: Iterable[
            PipelineStage[ContextT]
        ],
    ) -> None:

        self._stages.extend(stages)

    def remove_stage(
        self,
        stage: PipelineStage[ContextT],
    ) -> None:

        self._stages.remove(stage)

    def clear(
        self,
    ) -> None:

        self._stages.clear()

    def copy(
        self,
    ) -> "Pipeline[ContextT]":

        return type(self)(
            name=self.name,
            description=self.description,
            enabled=self.enabled,
            _stages=[
                stage.copy()
                for stage in self._stages
            ],
        )

    def __contains__(
        self,
        value: object,
    ) -> bool:

        return value in self._stages

    def __len__(
        self,
    ) -> int:

        return len(self._stages)

    def __iter__(
        self,
    ) -> Iterator[
        PipelineStage[ContextT]
    ]:

        return iter(self._stages)