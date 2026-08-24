from __future__ import annotations
from typing import List, Sequence

from core.request.middleware.registry import MiddlewareRegistry
from core.lifecycle.manager import LifecycleManager
from core.request.middleware.typing import MiddlewareType
from core.request.middleware.config import MiddlewareConfig, MiddlewareSpec

from .chain import MiddlewareChain
from .base import RequestMiddleware


class MiddlewareManager:

    __slots__ = (
        "_registry",
        "_lifecycle",
        "_instances",
    )

    def __init__(
        self,
        registry: MiddlewareRegistry,
        lifecycle: LifecycleManager,
    ) -> None:

        self._registry = registry
        self._lifecycle = lifecycle
        self._instances: dict[
            MiddlewareType,
            RequestMiddleware,
        ] = {}

    async def get(
        self,
        type_: MiddlewareType,
        config: MiddlewareConfig | None = None,
    ) -> RequestMiddleware:

        middleware = self._instances.get(
            type_,
        )

        if middleware is not None:
            return middleware

        middleware = self._registry.create(
            type_,
            config,
        )

        await self._lifecycle.acquire(
            middleware,
        )

        self._instances[
            type_
        ] = middleware

        return middleware

    def contains(
        self,
        type_: MiddlewareType,
    ) -> bool:

        return type_ in self._instances

    def values(
        self,
    ) -> tuple[RequestMiddleware, ...]:

        return tuple(
            self._instances.values(),
        )

    def ordered(
        self,
    ) -> tuple[RequestMiddleware, ...]:

        return tuple(
            sorted(
                (
                    middleware
                    for middleware
                    in self._instances.values()
                    if middleware.config.enabled
                ),
                key=lambda middleware: (
                    middleware.config.priority,
                    middleware.name,
                ),
            ),
        )

    async def build_chain(
        self,
        configs: Sequence[MiddlewareSpec],
    ) -> MiddlewareChain:

        middlewares: List[RequestMiddleware] = []

        for item in configs:
            middleware = await self.get(
                item.type,
                item.config,
            )

            middlewares.append(
                middleware,
            )

        return MiddlewareChain(
            self.ordered(),
        )