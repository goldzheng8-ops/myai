from typing import Any

from core.event import EventDispatcher, EventRegistry
from core.provider import ProviderBuilder
from core.provider.protocol import ProviderResolver
from core.request.events.completed import RequestCompleted
from core.request.events.failed import RequestFailed
from core.request.events.skipped import RequestSkipped
from core.request.events.started import RequestStarted
from core.request.handlers.completed import RequestCompletedHandler
from core.request.handlers.failed import RequestFailedHandler
from core.request.handlers.skipped import RequestSkippedHandler
from core.request.handlers.started import RequestStartedHandler


def register_events(
    builder: ProviderBuilder,
) -> None:

    builder.add_type(
        RequestStartedHandler,
    )

    builder.add_type(
        RequestCompletedHandler,
    )

    builder.add_type(
        RequestFailedHandler,
    )

    builder.add_type(
        RequestSkippedHandler,
    )

    builder.add_factory(
        EventRegistry,
        build_event_registry,
    )

    builder.add_factory(
        EventDispatcher,
        lambda resolver: EventDispatcher(
            registry=resolver.resolve(
                EventRegistry,
            ),
        ),
    )

def build_event_registry(
    resolver: ProviderResolver[Any, Any],
) -> EventRegistry:

    registry = EventRegistry()

    registry.add(
        RequestStarted,
        resolver.resolve(
            RequestStartedHandler,
        ),
    )

    registry.add(
        RequestCompleted,
        resolver.resolve(
            RequestCompletedHandler,
        ),
    )

    registry.add(
        RequestFailed,
        resolver.resolve(
            RequestFailedHandler,
        ),
    )

    registry.add(
        RequestSkipped,
        resolver.resolve(
            RequestSkippedHandler,
        ),
    )

    registry.freeze()

    return registry