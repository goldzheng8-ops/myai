from core.event import EventDispatcher, EventRegistry
from core.provider import ProviderBuilder


def register_events(
    builder: ProviderBuilder,
) -> None:

    builder.add_type(
        EventRegistry,
    )

    builder.add_factory(
        EventDispatcher,
        lambda resolver: EventDispatcher(
            registry=resolver.resolve(
                EventRegistry,
            ),
        ),
    )