from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import MiddlewareConfig
from core.request.middleware.typing import RequestMiddlewareNext
from core.request.middleware.throttle.policy import ThrottlePolicy
from core.request.middleware.throttle.resolver import ThrottleKeyResolver
from core.request.middleware.throttle.limiter import ThrottleLimiter

class ThrottleMiddleware(
    RequestMiddleware,
):

    def __init__(
        self,
        limiter: ThrottleLimiter,
        resolver: ThrottleKeyResolver,
        policy: ThrottlePolicy,
        config: MiddlewareConfig | None = None,
    ) -> None:
        super().__init__(
            config
            if config is not None
            else MiddlewareConfig(),
        )
        self._limiter = limiter

        self._resolver =resolver

        self._policy =policy

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        if not self._policy.enabled:
            return await next_(
                context,
            )

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