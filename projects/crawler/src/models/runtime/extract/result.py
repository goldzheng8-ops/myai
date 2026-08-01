from dataclasses import dataclass, field
from typing import Any

from models.runtime.base import BaseResult


@dataclass(slots=True)
class ExtractResult(BaseResult):

    data: Any = None
    
    metadata:dict[str, Any] = field(default_factory=dict)
