from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RequestMeta:
    """
    Runtime-independent control metadata for a request.
    """

    priority: int = 0

    retry: int = 0

    dont_filter: bool = False

    tags: set[str] = field(
        default_factory=set,
    )

    extras: dict[str, Any] = field(
        default_factory=dict,
    )