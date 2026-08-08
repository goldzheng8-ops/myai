from __future__ import annotations

from dataclasses import dataclass

from .typing import (
    RequestBody,
    RequestParams,
)


@dataclass(frozen=True, slots=True)
class RequestPatch:
    """
    Partial modifications applied to a request.
    """

    url: str | None = None

    params: RequestParams | None = None

    body: RequestBody | None = None