from __future__ import annotations

from dataclasses import dataclass

from core.event import Event

from ..descriptor import RequestDescriptor

@dataclass(frozen=True, slots=True)
class RequestSkipped(Event):

    request: RequestDescriptor
    reason: str