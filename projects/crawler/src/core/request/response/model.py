from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True, slots=True)
class RequestResponse:
    """
    Raw response produced by request execution.

    This model belongs to the request layer and contains only
    transport-level response data.
    """

    url: str

    status_code: int

    headers: Mapping[str, str] = field(
        default_factory=dict,
    )

    body: bytes = b""

    cookies: Mapping[str, str] = field(
        default_factory=dict,
    )

    encoding: str | None = None

    reason: str | None = None