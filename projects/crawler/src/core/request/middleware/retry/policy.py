from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """
    Controls retry behavior for a request.
    """

    max_attempts: int = 3

    delay: float = 0.0

    enabled: bool = True

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError(
                "max_attempts must be greater than or equal to 1."
            )

        if self.delay < 0:
            raise ValueError(
                "delay must be greater than or equal to 0."
            )