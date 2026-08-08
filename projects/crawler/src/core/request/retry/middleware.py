from core.request.context import RequestContext
from core.request.middleware.protocol import (
    RequestMiddleware,
    RequestMiddlewareNext,
)


class RetryMiddleware(
    RequestMiddleware,
):

    name = "retry"

    priority = 200

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        try:

            return await next_(
                context,
            )

        except Exception:

            # retry logic

            raise