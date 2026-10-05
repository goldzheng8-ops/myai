# core/event/handler.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Protocol

from .event import Event
from .typing import ContextT

class EventHandler(
    Protocol[ContextT],
):
    """
    Protocol for event handlers.

    A handler receives an Event and a runtime context,
    and returns the updated context.
    """

    async def handle(
        self,
        event: Event,
        context: ContextT,
    ) -> ContextT:
        ...

@dataclass(frozen=True, slots=True)
class EventHandlerRegistration(
    Generic[ContextT],
):
    """
    Registration metadata for an event handler.
    """

    handler: EventHandler[ContextT]

    priority: int = 0

    enabled: bool = True

    name: str | None = None