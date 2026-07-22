from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, kw_only=True)
class BaseResult:

    elapsed: float = 0.0

    meta: dict[str, Any] = field(default_factory=dict)

    trace: list[str] = field(default_factory=list)