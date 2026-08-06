from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from core.event.context import EventContext


@dataclass(slots=True)
class Event:
    context: EventContext
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if self.context is None:
            self.context = EventContext({})

    @property
    def data(self) -> dict[str, object]:
        return dict(self.context.data)