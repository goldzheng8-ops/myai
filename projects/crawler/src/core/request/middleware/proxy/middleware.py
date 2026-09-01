from __future__ import annotations

from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import ProxyMiddlewareConfig
from core.request.middleware.typing import MiddlewareType, RequestMiddlewareNext
from core.request.patch import RequestPatch

from .provider import ProxyProvider
from .model import ProxyConfig


PROXY_RUNTIME_KEY = "request.proxy"


class ProxyMiddleware(
    RequestMiddleware[ProxyMiddlewareConfig],
):
    plugin_type = MiddlewareType.PROXY
    def __init__(
        self,
        provider: ProxyProvider,
        config: ProxyMiddlewareConfig,
    ) -> None:
        super().__init__(config)
        self._provider = provider

    @property
    def provider(
        self,
    ) -> ProxyProvider:
        return self._provider

    @property
    def config(
        self,
    ) -> ProxyMiddlewareConfig:
        return self._config

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        proxy = context.descriptor.proxy

        if proxy is not None and not self.config.override:
            context.runtime.set(
                PROXY_RUNTIME_KEY,
                proxy,
            )

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

        context.descriptor = RequestBuilder.from_patch(
            descriptor=context.descriptor,
            patch=RequestPatch(
                proxy=proxy,
            ),
        )

        context.runtime.set(
            PROXY_RUNTIME_KEY,
            proxy,
        )