from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.response.base import ResponseAdapter


@dataclass(slots=True)
class RequestResult:
    """
    Result produced by request execution.
    """

    response: ResponseAdapter | None = None

    value: Any = None

    error: Exception | None = None

    elapsed: float | None = None

    success: bool = False