from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeduplicatePolicy:
    """
    Controls whether request deduplication is enabled.
    """

    enabled: bool = True