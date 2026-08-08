from __future__ import annotations

import asyncio
from typing import Any

from .event import Event
from .handler import EventHandler
from .registry import EventRegistry


class EventDispatcher:
    """
    Dispatch events to registered handlers.

    EventDispatcher is intentionally lightweight:
    it is responsible only for notification delivery,
    not for request/workflow execution orchestration.
    """

    def __init__(
        self,
        registry: EventRegistry,
    ) -> None:

        self._registry = registry

    @property
    def registry(
        self,
    ) -> EventRegistry:

        return self._registry

    async def emit(
        self,
        event: Event,
    ) -> None:
        """
        Emit an event sequentially.

        Handlers are invoked in registry order.
        """

        handlers = self._get_handlers(
            event,
        )

        for handler in handlers:

            await handler.handle(
                event,
            )

    async def emit_parallel(
        self,
        event: Event,
    ) -> None:
        """
        Emit an event to all handlers concurrently.

        All handlers are scheduled at the same time.
        Exceptions are propagated according to
        asyncio.gather() semantics.
        """

        handlers = self._get_handlers(
            event,
        )

        if not handlers:
            return

        await asyncio.gather(
            *(
                handler.handle(event)
                for handler in handlers
            ),
        )

    def _get_handlers(
        self,
        event: Event,
    ) -> tuple[EventHandler[Any], ...]:

        return self._registry.get(
            type(event),
        )