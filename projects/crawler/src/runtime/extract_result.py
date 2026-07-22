from dataclasses import dataclass, field
from typing import Any

from runtime.base import BaseResult


@dataclass(slots=True)
class ExtractResult(BaseResult):

    items: list[dict[str, Any]] = field(default_factory=list)