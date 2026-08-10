from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ThrottlePolicy:
    """
    Policy controlling whether request throttling is enabled.
    """

    enabled: bool = True