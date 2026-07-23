from dataclasses import dataclass, field

from enums.merge_policy import MergePolicy
from request.merger import MappingMerger, MergeRule, ValueMerger


@dataclass(slots=True)
class RequestMergeConfig:

    rules: list[MergeRule] = field(
        default_factory=lambda: [

            MergeRule(
                "headers",
                MappingMerger,
                MergePolicy.MERGE,
            ),

            MergeRule(
                "cookies",
                MappingMerger,
                MergePolicy.MERGE,
            ),

            MergeRule(
                "params",
                MappingMerger,
                MergePolicy.MERGE,
            ),

            MergeRule(
                "body",
                ValueMerger,
                MergePolicy.REPLACE,
            ),

            MergeRule(
                "method",
                ValueMerger,
                MergePolicy.REPLACE,
            ),

            MergeRule(
                "timeout",
                ValueMerger,
                MergePolicy.REPLACE,
            ),

            MergeRule(
                "retry",
                ValueMerger,
                MergePolicy.REPLACE,
            ),

            MergeRule(
                "proxy",
                ValueMerger,
                MergePolicy.REPLACE,
            ),
        ]
    )