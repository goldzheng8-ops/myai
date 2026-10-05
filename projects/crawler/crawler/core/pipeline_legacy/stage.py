from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import Generic

from .descriptor import PipelineDescriptor
from .step import PipelineStep
from .typing import ContextT


@dataclass(slots=True)
class PipelineStage(
    PipelineDescriptor,
    Generic[ContextT],
):

    _steps: list[
        PipelineStep[ContextT]
    ] = field(
        default_factory=list,
    )

    @property
    def steps(
        self,
    ) -> tuple[
        PipelineStep[ContextT],
        ...
    ]:

        return tuple(self._steps)

    def contains(
        self,
        value: PipelineStep[ContextT],
    ) -> bool:

        return value in self._steps

    def add_step(
        self,
        step: PipelineStep[ContextT],
    ) -> None:

        self._steps.append(step)

    def extend(
        self,
        steps: Iterable[
            PipelineStep[ContextT]
        ],
    ) -> None:

        self._steps.extend(steps)

    def remove_step(
        self,
        step: PipelineStep[ContextT],
    ) -> None:

        self._steps.remove(step)

    def clear(
        self,
    ) -> None:

        self._steps.clear()

    def copy(
        self,
    ) -> "PipelineStage[ContextT]":

        return type(self)(
            name=self.name,
            description=self.description,
            enabled=self.enabled,
            _steps=[
                step.copy()
                for step in self._steps
            ],
        )

    def __contains__(
        self,
        value: object,
    ) -> bool:

        return value in self._steps

    def __len__(
        self,
    ) -> int:

        return len(self._steps)

    def __iter__(
        self,
    ) -> Iterator[
        PipelineStep[ContextT]
    ]:

        return iter(self._steps)