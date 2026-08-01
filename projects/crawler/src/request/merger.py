from core.merger.rule import MergeRule
from models.config.request import RequestConfig
from models.runtime.request.descriptor import RequestDescriptor
from typing import Sequence


from .defaults import DEFAULT_REQUEST_MERGE_RULES


class RequestMerger:
    """
    Merge a RequestDescriptor into a RequestConfig.

    RequestMerger itself knows nothing about merge algorithms.
    It only coordinates MergeRule execution.
    """

    def __init__(
        self,
        rules: Sequence[MergeRule] = DEFAULT_REQUEST_MERGE_RULES,
    ) -> None:

        self._rules = tuple(rules)

    def merge(
        self,
        parent: RequestConfig,
        descriptor: RequestDescriptor,
    ) -> RequestConfig:

        request = parent.model_copy(
            deep=True,
        )

        for rule in self._rules:

            self._merge_field(
                request,
                descriptor,
                rule,
            )

        return request

    def _merge_field(
        self,
        request: RequestConfig,
        descriptor: RequestDescriptor,
        rule: MergeRule,
    ) -> None:

        parent_value = getattr(
            request,
            rule.field,
        )

        child_value = getattr(
            descriptor,
            rule.field,
        )

        merged = rule.merger.merge(
            parent_value,
            child_value,
        )

        setattr(
            request,
            rule.field,
            merged,
        )