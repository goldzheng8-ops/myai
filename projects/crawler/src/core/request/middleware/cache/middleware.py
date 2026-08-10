from __future__ import annotations

from core.cache.protocol import Cache

from core.request.context import RequestContext
from core.request.middleware.base import (
    RequestMiddleware,
    RequestMiddlewareNext,
)
from core.request.response import RequestResponse
from core.request.result import RequestResult

from .key import (
    CacheKeyProvider,
    FingerprintCacheKeyProvider,
)
from .policy import CachePolicy


class CacheMiddleware(
    RequestMiddleware,
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
        policy: CachePolicy | None = None,
        key_provider: CacheKeyProvider | None = None,
    ) -> None:

        self._cache = cache

        self._policy = (
            policy
            if policy is not None
            else CachePolicy()
        )

        self._key_provider = (
            key_provider
            if key_provider is not None
            else FingerprintCacheKeyProvider()
        )

    @property
    def cache(
        self,
    ) -> Cache[str, RequestResponse]:

        return self._cache

    @property
    def policy(
        self,
    ) -> CachePolicy:

        return self._policy

    @property
    def key_provider(
        self,
    ) -> CacheKeyProvider:

        return self._key_provider

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        method = context.descriptor.method

        if not self._policy.allows(method):
            return await next_(context)

        key = self._key_provider.build(
            context,
        )

        if self._policy.read:

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

        if self._policy.write:
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