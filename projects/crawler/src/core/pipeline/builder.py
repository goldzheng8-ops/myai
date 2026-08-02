from typing import Generic, Self

from core.pipeline.pipeline import DefaultPipeline
from core.pipeline.executor import PipelineExecutor
from core.pipeline.middleware import PipelineMiddleware
from core.pipeline.registry import MiddlewareRegistry
from core.pipeline.typing import ContextT



class PipelineBuilder(
    Generic[ContextT],
):

    def __init__(self) -> None:

        self._registry = MiddlewareRegistry[
            ContextT
        ]()

    def add(
        self,
        middleware: PipelineMiddleware[ContextT],
    ) -> Self:

        self._registry.add(
            middleware,
        )

        return self

    def insert(
        self,
        index: int,
        middleware: PipelineMiddleware[ContextT],
    ) -> Self:

        self._registry.insert(
            index,
            middleware,
        )

        return self

    def clear(self) -> Self:

        self._registry.clear()

        return self

    def build(
        self,
        executor: PipelineExecutor[
            ContextT,
        ],
    ) -> DefaultPipeline[
        ContextT,
    ]:
        return DefaultPipeline(
            registry=self._registry,
            executor=executor,
        )