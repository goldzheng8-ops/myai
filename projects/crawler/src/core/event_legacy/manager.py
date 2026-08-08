from __future__ import annotations

from .dispatcher import EventDispatcher
from .event import Event
from .handler import EventHandler
from .mode import DispatchMode
from .provider import EventHandlerProvider
from .registry import EventRegistry


class EventManager:
    def __init__(
        self,
        registry: EventRegistry | None = None,
        provider: EventHandlerProvider | None = None,
        dispatch_mode: DispatchMode = DispatchMode.SEQUENTIAL,
    ) -> None:
        self._registry = registry or EventRegistry()
        self._dispatcher = EventDispatcher(
            registry=self._registry,
            provider=provider,
            dispatch_mode=dispatch_mode,
        )

    @property
    def registry(self) -> EventRegistry:
        return self._registry

    def register(
        self,
        event_type: type[Event],
        handler: type[EventHandler],
    ) -> "EventManager":
        self._registry.register(event_type, handler)
        return self

    def add(
        self,
        handler: type[EventHandler],
        event_type: type[Event] | None = None,
    ) -> "EventManager":
        resolved_event = event_type or getattr(handler, "event", None)
        if resolved_event is None:
            raise ValueError(
                "Event type for handler is not defined. "
                "Pass it explicitly or declare an 'event' attribute."
            )

        self._registry.register(resolved_event, handler)
        return self

    def contains(self, event_type: type[Event]) -> bool:
        return self._registry.contains(event_type)

    async def dispatch(self, event: Event) -> None:
        await self._dispatcher.dispatch(event)

    async def emit(self, event: Event) -> None:
        await self.dispatch(event)
