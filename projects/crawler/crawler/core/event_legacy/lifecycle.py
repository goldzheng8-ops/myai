from __future__ import annotations

from typing import Generic, Sequence

from .dispatcher import EventDispatcher
from .event import Event
from .middleware import (
    EventMiddleware,
    EventMiddlewareNext,
)
from .typing import ContextT


class EventLifecycle(
    Generic[ContextT],
):
    """
    Coordinates event middleware and dispatching.

    Middleware wraps the dispatcher using an onion-style
    execution chain.
    """

    def __init__(
        self,
        dispatcher: EventDispatcher[ContextT],
        middleware: Sequence[
            EventMiddleware[ContextT]
        ] = (),
    ) -> None:

        self._dispatcher = dispatcher

        self._middleware = tuple(
            middleware
        )

        self._chain = self._build_chain()

    @property
    def dispatcher(
        self,
    ) -> EventDispatcher[ContextT]:

        return self._dispatcher

    @property
    def middleware(
        self,
    ) -> tuple[
        EventMiddleware[ContextT],
        ...,
    ]:

        return self._middleware

    async def dispatch(
        self,
        event: Event,
        context: ContextT,
    ) -> ContextT:

        return await self._chain(
            event,
            context,
        )

    def _build_chain(
        self,
    ) -> EventMiddlewareNext[ContextT]:

        async def dispatch(
            event: Event,
            context: ContextT,
        ) -> ContextT:

            return await self._dispatcher.dispatch(
                event,
                context,
            )

        next_ = dispatch

        for middleware in reversed(
            self._middleware
        ):

            current = middleware
            previous = next_

            async def invoke(
                event: Event,
                context: ContextT,
                *,
                current: EventMiddleware[ContextT] = current,
                previous: EventMiddlewareNext[
                    ContextT
                ] = previous,
            ) -> ContextT:

                return await current.process(
                    event,
                    context,
                    previous,
                )

            next_ = invoke

        return next_