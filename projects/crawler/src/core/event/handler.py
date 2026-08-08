from __future__ import annotations
from dataclasses import dataclass

from typing import Protocol

from .event import Event
from .typing import EventT


class EventHandler(
    Protocol[EventT],
):

    async def handle(
        self,
        event: EventT,
    ) -> None:
        """
        Handle an event notification.

        Handlers must not control the main execution flow.
        """
        ...



@dataclass(frozen=True, slots=True)
class RequestCompleted(Event):

    request_id: str
    status_code: int


class MetricsHandler(
    EventHandler[RequestCompleted],
):

    async def handle(
        self,
        event: RequestCompleted,
    ) -> None:

        print(
            event.request_id,
            event.status_code,
        )