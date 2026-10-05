from __future__ import annotations

from dataclasses import dataclass

from core.event import Event

from ..descriptor import RequestDescriptor
from ..result import RequestResult


@dataclass(frozen=True, slots=True)
class RequestCompleted(Event):
    """
    Emitted when a request completes successfully.
    """

    request: RequestDescriptor

    result: RequestResult