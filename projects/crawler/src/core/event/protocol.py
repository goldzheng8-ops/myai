from typing import Any

from core.provider.protocol import MultiResolver
from core.event.handler import EventHandler
from core.event.event import Event
class EventResolver(
    MultiResolver[
        type[Event],
        EventHandler[Any],
    ],
):
    pass

    EventPublisher
    
    EventDispatcherProtocol

