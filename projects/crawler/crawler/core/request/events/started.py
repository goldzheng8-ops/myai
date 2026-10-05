from __future__ import annotations

from dataclasses import dataclass

from core.event import Event

from ..descriptor import RequestDescriptor


@dataclass(frozen=True, slots=True)
class RequestStarted(Event):
    """
    Emitted when a request starts execution.
    """

    request: RequestDescriptor