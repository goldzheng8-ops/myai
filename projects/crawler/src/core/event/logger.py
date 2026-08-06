from __future__ import annotations

import logging

from .event import Event
from .handler import EventHandler


class LoggerHandler(EventHandler[Event]):
    event = Event
    priority = 100

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(__name__)

    async def handle(self, event: Event) -> None:
        self._logger.info("Dispatch %s at %s", event.__class__.__name__, event.timestamp)