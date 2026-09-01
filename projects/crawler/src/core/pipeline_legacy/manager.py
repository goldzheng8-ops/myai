from collections.abc import Iterable
from typing import Generic

from .pipeline import Pipeline
from .registry import PipelineRegistry
from .typing import ContextT


class PipelineManager(
    Generic[ContextT],
):

    def __init__(
        self,
        pipelines: Iterable[
            Pipeline[ContextT]
        ] = (),
    ) -> None:

        self._registry = PipelineRegistry[ContextT]()

        for pipeline in pipelines:
            self.register(pipeline)

    @property
    def registry(
        self,
    ) -> PipelineRegistry[
        ContextT
    ]:

        return self._registry

    def register(
        self,
        pipeline: Pipeline[ContextT],
        name: str | None = None,
    ) -> None:

        self._registry.register(
            name or pipeline.name,
            pipeline,
        )

    def get(
        self,
        name: str,
    ) -> Pipeline[
        ContextT
    ]:

        return self._registry.get(name)

    def contains(
        self,
        name: str,
    ) -> bool:

        return self._registry.contains(name)

    def clear(
        self,
    ) -> None:

        self._registry.clear()