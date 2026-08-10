from __future__ import annotations

import asyncio
from dataclasses import dataclass

from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.typing import RequestMiddlewareNext
from core.request.result import RequestResult

from .policy import DeduplicatePolicy


@dataclass(frozen=True, slots=True)
class DeduplicateOutcome:
    """
    Shared outcome of an in-flight request.
    """

    result: RequestResult | None = None

    exception: BaseException | None = None

    @classmethod
    def success(
        cls,
        result: RequestResult,
    ) -> DeduplicateOutcome:

        return cls(
            result=result,
        )

    @classmethod
    def failure(
        cls,
        exception: BaseException,
    ) -> DeduplicateOutcome:

        return cls(
            exception=exception,
        )

    def raise_if_failed(
        self,
    ) -> None:

        if self.exception is not None:
            raise self.exception


class DeduplicateMiddleware(
    RequestMiddleware,
):

    def __init__(
        self,
        policy: DeduplicatePolicy | None = None,
    ) -> None:

        self._policy = (
            policy
            if policy is not None
            else DeduplicatePolicy()
        )

        self._in_flight: dict[
            str,
            asyncio.Future[DeduplicateOutcome],
        ] = {}

        self._lock = asyncio.Lock()

    @property
    def policy(
        self,
    ) -> DeduplicatePolicy:

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

        fingerprint = context.fingerprint

        if fingerprint is None:
            return await next_(
                context,
            )

        future, owner = await self._acquire(
            fingerprint,
        )

        if not owner:

            outcome = await asyncio.shield(
                future,
            )

            outcome.raise_if_failed()

            if outcome.result is None:
                raise RuntimeError(
                    "Deduplication completed without a result."
                )

            context.result = outcome.result

            return context

        return await self._execute_owner(
            context=context,
            next_=next_,
            fingerprint=fingerprint,
            future=future,
        )

    async def _acquire(
        self,
        fingerprint: str,
    ) -> tuple[
        asyncio.Future[DeduplicateOutcome],
        bool,
    ]:

        loop = asyncio.get_running_loop()

        async with self._lock:

            future = self._in_flight.get(
                fingerprint,
            )

            if future is not None:
                return future, False

            future = loop.create_future()

            self._in_flight[
                fingerprint
            ] = future

            return future, True

    async def _execute_owner(
        self,
        *,
        context: RequestContext,
        next_: RequestMiddlewareNext,
        fingerprint: str,
        future: asyncio.Future[
            DeduplicateOutcome
        ],
    ) -> RequestContext:

        try:

            result_context = await next_(
                context,
            )

            result = result_context.result

            if result is None:
                raise RuntimeError(
                    "Request completed without a result."
                )

            future.set_result(
                DeduplicateOutcome.success(
                    result,
                ),
            )

            return result_context

        except asyncio.CancelledError as exc:

            if not future.done():

                future.set_result(
                    DeduplicateOutcome.failure(
                        exc,
                    ),
                )

            raise

        except Exception as exc:

            if not future.done():

                future.set_result(
                    DeduplicateOutcome.failure(
                        exc,
                    ),
                )

            raise

        finally:

            await self._release(
                fingerprint,
                future,
            )

    async def _release(
        self,
        fingerprint: str,
        future: asyncio.Future[
            DeduplicateOutcome
        ],
    ) -> None:

        async with self._lock:

            current = self._in_flight.get(
                fingerprint,
            )

            if current is future:

                del self._in_flight[
                    fingerprint
                ]