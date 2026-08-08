from __future__ import annotations

from dataclasses import dataclass

from core.event import Event

from ..descriptor import RequestDescriptor
from ..result import RequestResult


@dataclass(frozen=True, slots=True)
class RequestFailed(Event):
    """
    Emitted when a request execution fails.
    """

    request: RequestDescriptor

    error: Exception

    result: RequestResult | None = None