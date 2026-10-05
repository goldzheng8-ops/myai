from dataclasses import dataclass, field
from typing import Any, Sequence


@dataclass(slots=True, kw_only=True)
class BaseResult:
    """
    Base result shared by executable components.
    """

    success: bool = False
    error: Exception | None = None
    elapsed: float = 0.0
    meta: dict[str, Any] = field(default_factory=dict)
    trace: Sequence[Any] = ()