from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import ThrottleMiddlewareConfig
from core.request.middleware.typing import MiddlewareType, RequestMiddlewareNext
from core.request.middleware.throttle.resolver import ThrottleKeyResolver
from core.request.middleware.throttle.limiter import ThrottleLimiter

class ThrottleMiddleware(
    RequestMiddleware[ThrottleMiddlewareConfig],
):
    plugin_type = MiddlewareType.THROTTLE
    def __init__(
        self,
        limiter: ThrottleLimiter,
        resolver: ThrottleKeyResolver,
        config: ThrottleMiddlewareConfig,
    ) -> None:
        super().__init__(
            config
        )
        self._limiter = limiter

        self._resolver =resolver
    @property
    def config(self) -> ThrottleMiddlewareConfig:
        return self._config
    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        key = self._resolver.resolve(
            context,
        )

        await self._limiter.acquire(
            key,
        )

        try:

            return await next_(
                context,
            )

        finally:

            self._limiter.release(
                key,
            )