from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeAlias, TypeVar

if TYPE_CHECKING:
    from .event import Event
    
EventT = TypeVar(
    "EventT",
    bound="Event",
    contravariant=True,
)

EventMetadata: TypeAlias = dict[str, Any]