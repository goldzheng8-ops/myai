from __future__ import annotations
import logging

from core.event import Event, EventDispatcher
from core.request.result import RequestResult

from ..context import RequestContext
from ..events import (
    RequestCompleted,
    RequestFailed,
    RequestStarted,
)
from ..middleware import MiddlewareChain

from .base import RequestExecutor

logger = logging.getLogger(__name__)

class RequestRunner:
    """
    Coordinates the complete lifecycle of a request.
    """

    def __init__(
        self,
        executor: RequestExecutor,
        middleware: MiddlewareChain,
        dispatcher: EventDispatcher | None = None,
    ) -> None:

        self._executor = executor
        self._middleware = middleware
        self._dispatcher = dispatcher

    @property
    def executor(
        self,
    ) -> RequestExecutor:

        return self._executor

    @property
    def middleware(
        self,
    ) -> MiddlewareChain:

        return self._middleware

    @property
    def dispatcher(
        self,
    ) -> EventDispatcher | None:

        return self._dispatcher

    async def run(
        self,
        context: RequestContext,
    ) -> RequestContext:

        context.state.start()

        await self._notify(
            RequestStarted(
                request=context.descriptor,
            ),
        )

        try:

            context = await self._middleware.execute(
                context,
                self._executor.execute,
            )

            result = self._require_result(
                context,
            )

        except Exception as exc:

            context.state.fail(
                exc,
            )

            await self._notify(
                RequestFailed(
                    request=context.descriptor,
                    error=exc,
                    result=context.result,
                ),
            )

            raise

        context.state.complete()

        await self._notify(
            RequestCompleted(
                request=context.descriptor,
                result=result,
            ),
        )

        return context

    async def _notify(
        self,
        event: Event,
    ) -> None:

        if self._dispatcher is None:
            return

        try:

            await self._dispatcher.emit(
                event,
            )

        except Exception:
            logger.exception(
                "Request event handler failed: %s",
                type(event).__name__,
            )

    def _require_result(
        self,
        context: RequestContext,
    ) -> RequestResult:

        result = context.result

        if result is None:
            raise RuntimeError(
                "Request executor completed without producing "
                "a RequestResult.",
            )

        return result