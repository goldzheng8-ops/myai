from collections.abc import Mapping
from dataclasses import field,dataclass
from typing import Any

@dataclass(frozen=True, slots=True)
class OutputItem:
    data: Any
    spider: str
    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )