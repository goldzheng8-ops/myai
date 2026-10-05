from __future__ import annotations
from typing import Any

from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import ProxyMiddlewareConfig
from core.request.middleware.typing import MiddlewareType, RequestMiddlewareNext
from core.request.patch import RequestPatch

from .provider import ProxyProvider




class ProxyMiddleware(
    RequestMiddleware[ProxyMiddlewareConfig],
):
    plugin_type = MiddlewareType.PROXY
    def __init__(
        self,
        provider: ProxyProvider[Any],
        config: ProxyMiddlewareConfig,
    ) -> None:

        super().__init__(config)

        self._provider = provider

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        descriptor = context.descriptor

        if (
            descriptor.proxy is not None
            and not self._config.override
        ):
            return await next_(context)

        proxy = await self._provider.get(context)

        if proxy is None:
            return await next_(context)

        context.descriptor = (
            RequestBuilder.from_patch(
                descriptor=descriptor,
                patch=RequestPatch(
                    proxy=proxy,
                ),
            )
        )

        return await next_(context)