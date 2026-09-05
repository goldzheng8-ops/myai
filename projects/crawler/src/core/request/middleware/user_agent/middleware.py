from __future__ import annotations
from typing import Any

from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import UserAgentMiddlewareConfig
from core.request.middleware.typing import RequestMiddlewareNext


from .provider import UserAgentProvider

class UserAgentMiddleware(
    RequestMiddleware[UserAgentMiddlewareConfig],
):
    def __init__(
        self,
        provider: UserAgentProvider[Any],
        config: UserAgentMiddlewareConfig,
    ) -> None:

        super().__init__(config)

        self._provider = provider

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:
        descriptor = context.descriptor
        headers = descriptor.headers

        if (
            not self._config.override
            and "User-Agent" in headers
        ):
            return await next_(context)

        user_agent = await self._provider.get(context)

        if user_agent is None:
            return await next_(context)

        context.descriptor = (
            RequestBuilder
            .from_descriptor(
                context.descriptor,
            )
            .merge_headers(
                {"User-Agent": user_agent},
                override=self._config.override,
            )
            .build()
        )

        return await next_(context)
    