from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Generic

from .event import Event
from .typing import ContextT
from core.runtime.context import RuntimeContext

EventMiddlewareNext = Callable[
    [Event, ContextT],
    Awaitable[ContextT],
]


class EventMiddleware(
    ABC,
    Generic[ContextT],
):
    """
    Base class for event middleware.

    Middleware wraps the complete event dispatch process.
    """

    @abstractmethod
    async def process(
        self,
        event: Event,
        context: ContextT,
        next_: EventMiddlewareNext[ContextT],
    ) -> ContextT:
        """
        Process an event and optionally invoke the next middleware.
        """
        ...

class LoggingMiddleware(
    EventMiddleware[RuntimeContext],
):

    async def process(
        self,
        event: Event,
        context: RuntimeContext,
        next_: EventMiddlewareNext[RuntimeContext],
    ) -> RuntimeContext:

        print(
            f"Event started: {event.key}"
        )

        try:

            result = await next_(
                event,
                context,
            )

            print(
                f"Event completed: {event.key}"
            )

            return result

        except Exception:

            print(
                f"Event failed: {event.key}"
            )

            raise