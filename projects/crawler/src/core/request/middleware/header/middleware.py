from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.middleware.config import HeaderMiddlewareConfig

from core.request.middleware.base import RequestMiddleware
from core.request.middleware.typing import RequestMiddlewareNext
class HeaderMiddleware(
    RequestMiddleware[HeaderMiddlewareConfig],
):
    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        if not self._config.headers:
            return await next_(context)

        context.descriptor = (
            RequestBuilder
            .from_descriptor(
                context.descriptor,
            )
            .merge_headers(
                self._config.headers,
                override=self._config.override,
            )
            .build()
        )

        return await next_(context)