from __future__ import annotations

from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.typing import RequestMiddlewareNext

from .model import ProxyConfig
from .policy import ProxyPolicy
from .provider import ProxyProvider


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

        if not self._policy.override:

            existing = context.runtime.get(
                PROXY_RUNTIME_KEY,
            )

            if existing is not None:
                return

        context.runtime.set(
            PROXY_RUNTIME_KEY,
            proxy,
        )