from dataclasses import dataclass, field
from typing import Any

from runtime.base import BaseResult


@dataclass(slots=True)
class ExtractResult(BaseResult):

    data: dict[str, Any] = field(default_factory=dict)
    
    metadata:dict[str, Any] = field(default_factory=dict)
    warnings:list[str] = field(default_factory=list)
    errors:list[str] = field(default_factory=list)