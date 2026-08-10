from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CacheEntry:
    """
    Cached result data for a request.
    """

    content: str

    metadata: dict[str, Any]