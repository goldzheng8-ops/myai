from __future__ import annotations

from core.cache.protocol import Cache

from core.request.context import RequestContext
from core.request.middleware.typing import RequestMiddlewareNext
from core.request.middleware.base import (
    RequestMiddleware,
)
from core.request.middleware.config import CacheMiddlewareConfig
from core.request.response import RequestResponse
from core.request.result import RequestResult

from .key import (
    CacheKeyProvider,
)


class CacheMiddleware(
    RequestMiddleware[CacheMiddlewareConfig],
):
    """
    Request middleware providing response caching.

    The middleware caches transport-level RequestResponse
    objects and never caches ResponseAdapter instances.
    """

    def __init__(
        self,
        cache: Cache[str, RequestResponse],
        *,
        key_provider: CacheKeyProvider,
        config: CacheMiddlewareConfig,
    ) -> None:
        super().__init__(
            config,
        )
        self._cache = cache
        self._key_provider = key_provider

    @property
    def cache(
        self,
    ) -> Cache[str, RequestResponse]:

        return self._cache


    @property
    def key_provider(
        self,
    ) -> CacheKeyProvider:

        return self._key_provider
    @property
    def config(self) -> CacheMiddlewareConfig:
        return self._config
    
    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:
        config = self.config
        method = context.descriptor.method

        if method not in config.methods:
            return await next_(context)

        key = self._key_provider.build(
            context,
        )

        if config.read:

            cached = self._cache.get(
                key,
            )

            if cached is not None:
                self._restore_cached_response(
                    context,
                    cached,
                )

                return context

        context = await next_(
            context,
        )

        if config.write:
            self._store_response(
                key,
                context,
            )

        return context

    def _restore_cached_response(
        self,
        context: RequestContext,
        response: RequestResponse,
    ) -> None:

        context.result = RequestResult(
            response=response,
            success=True,
            elapsed=0.0,
        )

    def _store_response(
        self,
        key: str,
        context: RequestContext,
    ) -> None:

        result = context.result

        if result is None:
            return

        if not result.success:
            return

        response = result.response

        if response is None:
            return

        self._cache.put(
            key,
            response,
        )