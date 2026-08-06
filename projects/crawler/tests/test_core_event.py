from datetime import datetime

import pytest

from core.event import Event, EventBuilder, EventContext, EventDispatcher, EventManager, EventRegistry
from core.event.handler import EventHandler
from core.event.mode import DispatchMode


class DemoEvent(Event):
    pass


class RecordingHandler(EventHandler[DemoEvent]):
    event = DemoEvent
    calls: list[str] = []

    async def handle(self, event: DemoEvent) -> None:
        RecordingHandler.calls.append(event.context.data["value"])


@pytest.mark.asyncio
async def test_event_registry_and_dispatcher() -> None:
    registry = EventRegistry()
    registry.register(DemoEvent, RecordingHandler)

    event = DemoEvent(
        context=EventContext({"value": "hello"}),
        timestamp=datetime.now(),
    )

    dispatcher = EventDispatcher(
        registry=registry,
        provider=None,
        dispatch_mode=DispatchMode.SEQUENTIAL,
    )

    await dispatcher.dispatch(event)

    assert RecordingHandler.calls == ["hello"]


def test_event_builder_and_manager() -> None:
    builder = EventBuilder()
    builder.add(RecordingHandler)

    manager = builder.build()

    assert manager.contains(DemoEvent)
    assert DemoEvent in manager.registry

    RecordingHandler.calls.clear()
    event = DemoEvent(
        context=EventContext({"value": "builder"}),
        timestamp=datetime.now(),
    )

    assert manager.registry.contains(DemoEvent) is True

    import asyncio
    asyncio.run(manager.dispatch(event))

    assert RecordingHandler.calls == ["builder"]
