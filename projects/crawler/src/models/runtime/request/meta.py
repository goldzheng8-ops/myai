
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class RequestMeta:

    priority: int = 0

    retry: int = 0

    dont_filter: bool = False

    fingerprint: str | None = None

    tags: set[str] = field(
        default_factory=set,
    )

    extras: dict[str, Any] = field(
        default_factory=dict,
    )