from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic


from .typing import EventT

class EventHandler(
    ABC,
    Generic[EventT],
):
    """
    Base class for event handlers.
    """

    @abstractmethod
    async def handle(
        self,
        event: EventT,
    ) -> None:
        raise NotImplementedError


