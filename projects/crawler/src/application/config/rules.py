from core.merger import KeyedListMerger, RecursiveMappingMerger, ReplaceListMerger, ReplaceMerger
from core.merger.rule import MergeRule
from core.request.typing import RequestKind
from core.request.profile import RequestProfile
from core.typing.aliases import JsonDict


SPIDER_CONFIG_MERGE_RULES = (
    MergeRule(
        field="kind",
        merger=ReplaceMerger[RequestKind](),
    ),

    MergeRule(
        field="profile",
        merger=ReplaceMerger[RequestProfile](),
    ),

    MergeRule(
        field="start_requests",
        merger=ReplaceListMerger[JsonDict](),
    ),

    MergeRule(
        field="extraction",
        merger=ReplaceMerger[JsonDict](),
    ),

    MergeRule(
        field="discovery",
        merger=ReplaceListMerger[JsonDict](),
    ),

    MergeRule(
        field="middlewares",
        merger=KeyedListMerger(
            key="type",
            item_merger=RecursiveMappingMerger(),
        ),
    ),

    MergeRule(
        field="browser",
        merger=RecursiveMappingMerger(),
    ),

    MergeRule(
        field="settings",
        merger=RecursiveMappingMerger(),
    ),
)