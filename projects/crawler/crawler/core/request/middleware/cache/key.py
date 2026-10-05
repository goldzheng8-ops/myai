from __future__ import annotations

from typing import Protocol

from core.request.context import RequestContext


class CacheKeyProvider(Protocol):
    """
    Build a cache key for a request.
    """

    def build(
        self,
        context: RequestContext,
    ) -> str:
        ...


class FingerprintCacheKeyProvider(
    CacheKeyProvider,
):
    """
    Build cache keys from RequestContext.fingerprint.
    """

    prefix = "request"

    def build(
        self,
        context: RequestContext,
    ) -> str:

        fingerprint = context.fingerprint

        if fingerprint is None:
            raise ValueError(
                "RequestContext.fingerprint "
                "is required for caching."
            )

        return (
            f"{self.prefix}:{fingerprint}"
        )