# core/event/event.py

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from .typing import (
    EventKey,
    EventMetadata,
    EventPayload,
)


@dataclass(slots=True, frozen=True)
class Event:
    """
    Immutable event definition.

    An Event represents a single occurrence in the system.

    Parameters
    ----------
    key:
        Event identifier.

    payload:
        Event-specific data.

    metadata:
        Additional event metadata.
    """

    key: EventKey

    payload: EventPayload = None

    metadata: EventMetadata = field(
        default_factory=dict,
    )

    def __post_init__(self) -> None:

        if not self.key:
            raise ValueError(
                "Event key cannot be empty."
            )

    @property
    def metadata_view(
        self,
    ) -> Mapping[str, Any]:

        return MappingProxyType(
            self.metadata,
        )