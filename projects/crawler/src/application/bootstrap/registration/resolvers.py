from typing import Any

from core.extraction.resolver.plugins.expression import DefaultExpressionEvaluator
from core.extraction.resolver.plugins.template import DefaultTemplateManager
from core.extraction.selector.base import SelectorPipeline
from core.extraction.selector.executor import PipelineExecutor
from core.extraction.selector.extraction.registry import ExtractionRegistry
from core.extraction.selector.selection.registry import SelectionRegistry
from core.provider import ProviderBuilder,ProviderResolver
from core.extraction.resolver import (
    ResolverRegistry,
    create_constant_resolver,
    create_context_resolver,
    build_expression_resolver_factory,
    build_selector_resolver_factory,
    build_template_value_resolver_factory,
)
from core.extraction.value.typing import ValueType

def register_resolvers(
    builder: ProviderBuilder,
) -> None:

    # Resolver infrastructure
    builder.add_type(
        DefaultExpressionEvaluator,
    )

    builder.add_factory(
        PipelineExecutor,
        lambda resolver: SelectorPipeline(
            selections=resolver.resolve(
                SelectionRegistry,
            ),
            extractions=resolver.resolve(
                ExtractionRegistry,
            ),
        ),
    )

    builder.add_type(
        DefaultTemplateManager,
    )

    # Resolver registry
    builder.add_factory(
        ResolverRegistry,
        lambda resolver: create_resolver_registry(
            resolver,
        ),
    )


def create_resolver_registry(
    resolver: ProviderResolver[Any, Any],
) -> ResolverRegistry:

    registry = ResolverRegistry()

    registry.register(
        ValueType.CONSTANT,
        create_constant_resolver,
    )

    registry.register(
        ValueType.CONTEXT,
        create_context_resolver,
    )

    registry.register(
        ValueType.EXPRESSION,
        build_expression_resolver_factory(
            resolver,
        ),
    )

    registry.register(
        ValueType.SELECTOR,
        build_selector_resolver_factory(
            resolver,
        ),
    )

    registry.register(
        ValueType.TEMPLATE,
        build_template_value_resolver_factory(
            resolver,
        ),
    )

    return registry