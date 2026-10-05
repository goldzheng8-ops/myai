from dataclasses import dataclass
from typing import Any, Sequence

from .base import BaseMerger

@dataclass(
    frozen=True,
    slots=True,
)
class MergeRule:

    field: str

    merger: BaseMerger[Any]

class MergeRules:

    def __init__(
        self,
        rules: Sequence[MergeRule],
    ) -> None:

        self._rules = {
            rule.field: rule.merger
            for rule in rules
        }

    def get(
        self,
        field: str,
    ) -> BaseMerger[Any] | None:

        return self._rules.get(field)