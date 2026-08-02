from typing import Generic, Iterable

from core.pipeline.middleware import PipelineMiddleware
from .typing import ContextT

class MiddlewareRegistry(Generic[ContextT]):

    def __init__(
        self,
        middlewares: Iterable[
            PipelineMiddleware[ContextT]
        ] = (),
    ) -> None:
        self._middlewares = list(middlewares)

    def add(
        self,
        middleware: PipelineMiddleware[ContextT],
    ) -> None:
        self._middlewares.append(middleware)

    def insert(
        self,
        index: int,
        middleware: PipelineMiddleware[ContextT],
    ) -> None:
        self._middlewares.insert(index, middleware)

    def remove(
        self,
        middleware: PipelineMiddleware[ContextT],
    ) -> None:
        self._middlewares.remove(middleware)

    def clear(self) -> None:
        self._middlewares.clear()

    def middlewares(
        self,
    ) -> tuple[
        PipelineMiddleware[ContextT],
        ...
    ]:
        return tuple(self._middlewares)

    def __iter__(self) -> Iterable[PipelineMiddleware[ContextT]]:
        return iter(self._middlewares)

    def __len__(self) -> int:
        return len(self._middlewares)