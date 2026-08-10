from __future__ import annotations

from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.typing import RequestMiddlewareNext
from core.request.patch import RequestPatch

from .policy import ProxyPolicy
from .provider import ProxyProvider
from .model import ProxyConfig


PROXY_RUNTIME_KEY = "request.proxy"


class ProxyMiddleware(
    RequestMiddleware,
):

    def __init__(
        self,
        provider: ProxyProvider,
        policy: ProxyPolicy | None = None,
    ) -> None:

        self._provider = provider

        self._policy = (
            policy
            if policy is not None
            else ProxyPolicy()
        )

    @property
    def provider(
        self,
    ) -> ProxyProvider:

        return self._provider

    @property
    def policy(
        self,
    ) -> ProxyPolicy:

        return self._policy

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        if not self._policy.enabled:
            return await next_(
                context,
            )

        proxy = await self._provider.provide(
            context,
        )

        if proxy is not None:

            self._apply_proxy(
                context,
                proxy,
            )

        return await next_(
            context,
        )

    def _apply_proxy(
        self,
        context: RequestContext,
        proxy: ProxyConfig,
    ) -> None:

        existing = context.descriptor.proxy

        if existing is not None and not self._policy.override:
            context.runtime.set(
                PROXY_RUNTIME_KEY,
                context.descriptor.proxy,
            )
            return

        context.descriptor = (
            RequestBuilder.from_patch(
                descriptor=context.descriptor,
                patch=RequestPatch(
                    proxy=proxy,
                ),
            )
        )

        context.runtime.set(
            PROXY_RUNTIME_KEY,
            proxy,
        )