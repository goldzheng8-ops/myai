from typing import Any

from core.extraction.extractor.engine import ExtractEngine
from core.extraction.resolver.engine import ResolverExecutor
from core.extraction.transform.engine import TransformExecutor
from core.extraction.value.engine import ValueEngine
from core.extraction.value.evaluator import ValueExecutor
from core.provider import (
    ProviderBuilder,
    ProviderResolver,
)

from core.extraction.extractor import (
    build_field_extractor_factory,
    build_list_extractor_factory,
    build_object_extractor_factory,
    ExtractorRegistry,
    ExtractType,
    ExtractExecutor,
)

def register_extractors(
    builder: ProviderBuilder,
) -> None:
    builder.add_factory(
        ValueExecutor,
        lambda resolver: ValueEngine(
            resolver=resolver.resolve(
                ResolverExecutor,
            ),
            transformer=resolver.resolve(
                TransformExecutor,
            ),
        ),
    )

    builder.add_factory(
        ExtractExecutor,
        lambda resolver: ExtractEngine(
            registry=resolver.resolve(
                ExtractorRegistry,
            ),
        ),
    )

    builder.add_factory(
        ExtractorRegistry,
        lambda resolver: create_extractor_registry(
            resolver,
        ),
    )


def create_extractor_registry(
    resolver: ProviderResolver[Any, Any],
) -> ExtractorRegistry:

    registry = ExtractorRegistry()

    registry.register(
        ExtractType.FIELD,
        build_field_extractor_factory(
            resolver,
        ),
    )

    registry.register(
        ExtractType.LIST,
        build_list_extractor_factory(
            resolver,
        ),
    )

    registry.register(
        ExtractType.OBJECT,
        build_object_extractor_factory(
            resolver,
        ),
    )

    return registry
