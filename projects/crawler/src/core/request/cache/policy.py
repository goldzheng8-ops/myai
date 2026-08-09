from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CachePolicy:
    """
    Policy controlling request caching.
    """

    enabled: bool = True

    read: bool = True

    write: bool = True