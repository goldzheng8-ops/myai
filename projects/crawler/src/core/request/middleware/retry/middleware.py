from __future__ import annotations

import asyncio

from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import MiddlewareConfig
from core.request.middleware.typing import RequestMiddlewareNext

from .policy import RetryPolicy


class RetryMiddleware(
    RequestMiddleware,
):

    def __init__(
        self,
        policy: RetryPolicy,
        config: MiddlewareConfig | None = None,
    ) -> None:
        super().__init__(
            config
            if config is not None
            else MiddlewareConfig(),
        )
        self._policy =policy

    @property
    def policy(
        self,
    ) -> RetryPolicy:

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

        last_exception: BaseException | None = None

        for attempt in range(
            1,
            self._policy.max_attempts + 1,
        ):

            try:

                return await next_(
                    context,
                )

            except asyncio.CancelledError:

                raise

            except Exception as exc:

                last_exception = exc

                if attempt >= self._policy.max_attempts:
                    raise

                if self._policy.delay > 0:

                    await asyncio.sleep(
                        self._policy.delay,
                    )

        if last_exception is not None:
            raise last_exception

        raise RuntimeError(
            "RetryMiddleware exited without a result."
        )