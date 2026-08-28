from __future__ import annotations
import logging

from core.event import Event, EventDispatcher
from core.request.middleware.chain_builder import MiddlewareChainBuilder
from core.request.result import RequestResult

from .context import RequestContext
from .events import (
    RequestCompleted,
    RequestFailed,
    RequestStarted,
)


from .executor.base import RequestExecutor

logger = logging.getLogger(__name__)

class RequestRunner:

    def __init__(
        self,
        executor: RequestExecutor,
        middleware: MiddlewareChainBuilder,
        dispatcher: EventDispatcher | None = None,
    ) -> None:

        self._executor = executor
        self._middleware = middleware
        self._dispatcher = dispatcher

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

        chain = await self._middleware.build(
            context.configs,
        )
        try:

            context = await chain.execute(
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

        await self._dispatcher.emit(
            event,
        )

    @staticmethod
    def _require_result(
        context: RequestContext,
    ) -> RequestResult:

        result = context.result

        if result is None:
            raise RuntimeError(
                "Request executor completed without producing "
                "a RequestResult.",
            )

        return result