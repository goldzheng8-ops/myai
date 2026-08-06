from __future__ import annotations

import asyncio
from collections.abc import Sequence
from typing import Any

from .event import Event
from .handler import EventHandler
from .mode import DispatchMode
from .provider import EventHandlerProvider
from .registry import EventRegistry


class EventDispatcher:
    def __init__(
        self,
        registry: EventRegistry,
        provider: EventHandlerProvider | None,
        dispatch_mode: DispatchMode = DispatchMode.SEQUENTIAL,
    ) -> None:
        self._registry = registry
        self._provider = provider
        self._dispatch_mode = dispatch_mode

    def _resolve_handlers(
        self,
        event_type: type[Event],
    ) -> Sequence[EventHandler[Any]]:
        resolved: list[EventHandler[Any]] = []

        for candidate in event_type.__mro__:
            if candidate is object:
                continue

            if self._provider is not None and self._provider.contains(candidate):
                resolved.extend(self._provider.get(candidate))
                continue

            if self._registry.contains(candidate):
                handlers = self._registry.get(candidate)
                for handler_cls in handlers:
                    resolved.append(handler_cls())

        return tuple(dict.fromkeys(resolved))

    async def dispatch(
        self,
        event: Event,
    ) -> None:
        handlers = self._resolve_handlers(event.__class__)
        if not handlers:
            return

        if self._dispatch_mode is DispatchMode.PARALLEL:
            await asyncio.gather(*(handler.handle(event) for handler in handlers))
            return

        for handler in handlers:
            await handler.handle(event)

    async def emit(self, event: Event) -> None:
        await self.dispatch(event)

