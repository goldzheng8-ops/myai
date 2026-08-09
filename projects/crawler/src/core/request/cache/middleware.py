from core.request.context import RequestContext
from core.request.middleware.base import (
    RequestMiddleware,
    RequestMiddlewareNext,
)

class CacheMiddleware(
    RequestMiddleware,
):

    name = "cache"

    priority = 300

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        cached = ...

        if cached is not None:
            return cached

        result = await next_(
            context,
        )

        ...

        return result