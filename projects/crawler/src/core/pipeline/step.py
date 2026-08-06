from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import Generic

from .descriptor import PipelineDescriptor
from .pass_ import PipelinePass
from .typing import ContextT


@dataclass(slots=True)
class PipelineStep(
    PipelineDescriptor,
    Generic[ContextT],
):

    _passes: list[
        PipelinePass[ContextT]
    ] = field(
        default_factory=list,
    )

    @property
    def passes(
        self,
    ) -> tuple[
        PipelinePass[ContextT],
        ...
    ]:
        return tuple(self._passes)

    def contains(
        self,
        value: PipelinePass[ContextT],
    ) -> bool:

        return value in self._passes

    def add_pass(
        self,
        value: PipelinePass[ContextT],
    ) -> None:

        self._passes.append(value)

    def extend(
        self,
        values: Iterable[
            PipelinePass[ContextT]
        ],
    ) -> None:

        self._passes.extend(values)

    def remove_pass(
        self,
        value: PipelinePass[ContextT],
    ) -> None:

        self._passes.remove(value)

    def clear(
        self,
    ) -> None:

        self._passes.clear()

    def copy(
        self,
    ) -> "PipelineStep[ContextT]":

        return type(self)(
            name=self.name,
            description=self.description,
            enabled=self.enabled,
            _passes=self._passes.copy(),
        )

    def __contains__(
        self,
        value: object,
    ) -> bool:

        return value in self._passes

    def __len__(
        self,
    ) -> int:

        return len(self._passes)

    def __iter__(
        self,
    ) -> Iterator[
        PipelinePass[ContextT]
    ]:

        return iter(self._passes)