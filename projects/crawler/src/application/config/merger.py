from copy import deepcopy
from typing import Sequence,Any

from core.merger.rule import MergeRule
from pydantic import BaseModel


class ConfigMerger:

    def merge(
        self,
        parent: BaseModel,
        child: BaseModel,
        rules: Sequence[MergeRule],
    ) -> dict[str, Any]:

        parent_data = parent.model_dump(
            mode="python",
        )

        child_data = child.model_dump(
            mode="python",
            exclude_unset=True,
        )

        result = deepcopy(
            parent_data,
        )

        for rule in rules:

            if rule.field not in child_data:
                continue

            merger = rule.merger

            result[rule.field] = merger.merge(
                parent_data.get(rule.field),
                child_data[rule.field],
            )

        return result