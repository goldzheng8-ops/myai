from .provider import EventHandlerProvider
from .handler import EventHandler
from .event import Event
class ProviderEventResolver:

    def __init__(
        self,
        provider: EventHandlerProvider,
    ) -> None:

        self._provider = provider

    def resolve(
        self,
        event: type[Event],
    ) -> tuple[
        EventHandler[Event],
        ...,
    ]:

        return self._provider.get(event)