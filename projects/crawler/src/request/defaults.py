from core.merger.mapping import MappingMerger
from core.merger.rule import MergeRule

from core.merger.replace import ReplaceMerger


DEFAULT_REQUEST_MERGE_RULES = (
    MergeRule(
        "url",
        ReplaceMerger(),
    ),

    MergeRule(
        "headers",
        MappingMerger(),
    ),

    MergeRule(
        "cookies",
        MappingMerger(),
    ),

    MergeRule(
        "params",
        MappingMerger(),
    ),

    MergeRule(
        "body",
        ReplaceMerger(),
    ),

    MergeRule(
        "method",
        ReplaceMerger(),
    ),

    MergeRule(
        "timeout",
        ReplaceMerger(),
    ),

    MergeRule(
        "retry",
        ReplaceMerger(),
    ),

    MergeRule(
        "proxy",
        ReplaceMerger(),
    ),

    MergeRule(
        "meta",
        MappingMerger(),
    ),
)