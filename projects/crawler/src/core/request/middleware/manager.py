from __future__ import annotations
from typing import Any


from core.request.middleware.registry import MiddlewareRegistry
from core.lifecycle.manager import LifecycleManager
from core.request.middleware.typing import MiddlewareType
from core.request.middleware.config import  MiddlewareSpecUnion


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
            RequestMiddleware[Any],
        ] = {}

    async def get(
        self,
        spec: MiddlewareSpecUnion,
    ) -> RequestMiddleware[Any]:

        middleware = self._instances.get(
            spec.type,
        )

        if middleware is not None:
            return middleware

        middleware = self._registry.create(
            spec.type,
            spec.config,
        )

        await self._lifecycle.acquire(
            middleware,
        )

        self._instances[spec.type] = middleware

        return middleware
    
    def contains(
        self,
        type_: MiddlewareType,
    ) -> bool:

        return type_ in self._instances

    def values(
        self,
    ) -> tuple[RequestMiddleware[Any], ...]:

        return tuple(
            self._instances.values(),
        )

