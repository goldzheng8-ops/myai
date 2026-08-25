from collections.abc import Callable
from typing import Any, TypeAlias

from core.extraction.extractor.base import Extractor
from core.extraction.extractor.executor import ExtractExecutor
from core.extraction.extractor.field import FieldExtractor
from core.extraction.extractor.list import ListExtractor
from core.extraction.extractor.object import ObjectExtractor
from core.extraction.value.evaluator import ValueExecutor
from core.provider import ProviderResolver

ExtractorFactory: TypeAlias = Callable[
    [],
    Extractor[Any],
]

def build_field_extractor_factory(
    resolver: ProviderResolver[Any, Any],
) -> ExtractorFactory:

    def factory() -> FieldExtractor:
        return FieldExtractor(
            executor=resolver.resolve(
                ValueExecutor,
            ),
        )

    return factory

def build_list_extractor_factory(
    resolver: ProviderResolver[Any, Any],
) -> ExtractorFactory:

    def factory() -> ListExtractor:
        return ListExtractor(
            executor=resolver.resolve(
                ExtractExecutor,
            ),
        )

    return factory

def build_object_extractor_factory(
    resolver: ProviderResolver[Any, Any],
) -> ExtractorFactory:

    def factory() -> ObjectExtractor:
        return ObjectExtractor(
            executor=resolver.resolve(
                ExtractExecutor,
            ),
        )

    return factory