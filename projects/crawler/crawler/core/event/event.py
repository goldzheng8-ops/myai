from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .typing import EventMetadata


@dataclass(frozen=True, slots=True,kw_only=True)
class Event:
    """
    Base class for application events.

    An event represents something that has already happened.

    Events are immutable notifications and must not participate
    in the main execution flow.
    """

    metadata: EventMetadata = field(
        default_factory=dict,
    )

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc,
        ),
    )