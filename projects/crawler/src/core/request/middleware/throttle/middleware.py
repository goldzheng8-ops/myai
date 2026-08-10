from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.typing import RequestMiddlewareNext
from core.request.middleware.throttle.policy import ThrottlePolicy
from core.request.middleware.throttle.resolver import HostThrottleKeyResolver, ThrottleKeyResolver
from core.request.middleware.throttle.limiter import ThrottleLimiter

class ThrottleMiddleware(
    RequestMiddleware,
):

    def __init__(
        self,
        limiter: ThrottleLimiter,
        resolver: ThrottleKeyResolver | None = None,
        policy: ThrottlePolicy | None = None,
    ) -> None:

        self._limiter = limiter

        self._resolver = (
            resolver
            if resolver is not None
            else HostThrottleKeyResolver()
        )

        self._policy = (
            policy
            if policy is not None
            else ThrottlePolicy()
        )

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