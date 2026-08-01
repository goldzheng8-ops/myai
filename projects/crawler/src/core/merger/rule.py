from dataclasses import dataclass
from typing import Any

from .base import BaseMerger

@dataclass(
    frozen=True,
    slots=True,
)
class MergeRule:

    field: str

    merger: BaseMerger[Any]