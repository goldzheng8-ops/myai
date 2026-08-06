from __future__ import annotations

from typing import Any, Self

from .event import Event
from .handler import EventHandler
from .manager import EventManager
from .registry import EventRegistry


class EventBuilder:
    def __init__(
        self,
        registry: EventRegistry | None = None,
    ) -> None:
        self._registry = registry or EventRegistry()

    @property
    def registry(self) -> EventRegistry:
        return self._registry

    def add(
        self,
        handler: type[EventHandler[Any]],
        event_type: type[Event] | None = None,
    ) -> Self:
        resolved_event = event_type or getattr(handler, "event", None)
        if resolved_event is None:
            raise ValueError(
                f"Event type for handler {handler.__name__!r} is not defined. "
                "Pass the event type explicitly or declare an 'event' attribute."
            )

        self._registry.register(resolved_event, handler)
        return self

    def register(
        self,
        event_type: type[Event],
        handler: type[EventHandler[Any]],
    ) -> Self:
        self._registry.register(event_type, handler)
        return self

    def contains(self, event_type: type[Event]) -> bool:
        return self._registry.contains(event_type)

    def remove(
        self,
        event_type: type[Event],
        handler: type[EventHandler[Any]] | None = None,
    ) -> Self:
        self._registry.unregister(event_type, handler)
        return self

    def clear(self) -> Self:
        self._registry.clear()
        return self

    def build(self) -> EventManager:
        return EventManager(registry=self._registry)

    def clone(self) -> "EventBuilder":
        builder = EventBuilder(EventRegistry())
        builder._registry = self._registry.copy()
        return builder