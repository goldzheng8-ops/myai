from __future__ import annotations

from core.event import Event, EventDispatcher

from ..context import RequestContext
from ..events import (
    RequestCompleted,
    RequestFailed,
    RequestStarted,
)
from ..middleware import MiddlewareChain

from .executor import RequestExecutor


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

        await self._emit(
            RequestStarted(
                request=context.descriptor,
            ),
        )

        try:

            context = await self._middleware.execute(
                context,
                self._executor.execute,
            )

        except Exception as exc:

            context.state.error = exc

            await self._emit(
                RequestFailed(
                    request=context.descriptor,
                    error=exc,
                    result=context.result,
                ),
            )

            raise

        await self._emit(
            RequestCompleted(
                request=context.descriptor,
                result=context.result,
            ),
        )

        return context

    async def _emit(
        self,
        event: Event,
    ) -> None:

        if self._dispatcher is None:
            return

        await self._dispatcher.emit(
            event,
        )