from typing import Any

from core.registry.multi import MultiRegistry

from .event import Event
from .handler import EventHandler


class EventRegistry(
    MultiRegistry[
        type[Event],
        EventHandler[Any],
    ],
):
    """
    Registry mapping event types to handlers.
    """

    pass