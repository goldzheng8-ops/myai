from __future__ import annotations

import asyncio

from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import RetryMiddlewareConfig
from core.request.middleware.typing import RequestMiddlewareNext

class RetryMiddleware(
    RequestMiddleware[RetryMiddlewareConfig],
):

    def __init__(
        self,
        config: RetryMiddlewareConfig,
    ) -> None:
        super().__init__(
            config,
        )

    @property
    def config(
        self,
    ) -> RetryMiddlewareConfig:
        return self._config

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        for retry_number in range(
            self.config.max_retries + 1,
        ):
            try:
                return await next_(
                    context,
                )

            except asyncio.CancelledError:
                raise

            except Exception:

                if (
                    retry_number
                    >= self.config.max_retries
                ):
                    raise

                delay = self._calculate_delay(
                    retry_number,
                )

                if delay > 0:
                    await asyncio.sleep(
                        delay,
                    )

        raise RuntimeError(
            "RetryMiddleware exited without a result."
        )

    def _calculate_delay(
        self,
        retry_number: int,
    ) -> float:

        delay = (
            self.config.retry_delay
            * (
                self.config.backoff_factor
                ** retry_number
            )
        )

        if self.config.max_delay is not None:
            delay = min(
                delay,
                self.config.max_delay,
            )

        return delay