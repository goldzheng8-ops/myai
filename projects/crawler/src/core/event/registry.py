
from typing import Any

from core.registry.multi import MultiRegistry
from .event import Event
from .handler import EventHandler

class EventRegistry(
    MultiRegistry[
        type[Event],
        type[EventHandler[Any]],
    ],
):
    """
    Event → Handler types.
    """