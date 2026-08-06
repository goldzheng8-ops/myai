from typing import Any

from .handler import EventHandler
from .event import Event

from core.provider.multi import MultiProvider


class EventHandlerProvider(
    MultiProvider[
        type[Event],
        EventHandler[Any],
    ],
):
    """
    Resolves handlers of one event.
    """

    pass