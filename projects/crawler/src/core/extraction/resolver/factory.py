from collections.abc import Callable
from typing import Any, TypeAlias

from core.extraction.resolver.base import Resolver
from core.extraction.resolver.plugins.constant import ConstantResolver
from core.extraction.resolver.plugins.context import ContextResolver
from core.extraction.resolver.plugins.expression import DefaultExpressionEvaluator, ExpressionResolver
from core.extraction.resolver.plugins.selector import SelectorResolver
from core.extraction.resolver.plugins.template import DefaultTemplateManager, TemplateValueResolver
from core.provider import ProviderResolver
from core.extraction.selector.executor import PipelineExecutor

ResolverFactory: TypeAlias = Callable[
    [],
    Resolver[Any],
]

def create_constant_resolver() -> ConstantResolver:
    return ConstantResolver()

def create_context_resolver() -> ContextResolver:
    return ContextResolver()

def build_expression_resolver_factory(
    provider: ProviderResolver[Any, Any],
) -> ResolverFactory:

    def factory() -> ExpressionResolver:
        return ExpressionResolver(
            evaluator=provider.resolve(
                DefaultExpressionEvaluator,
            ),
        )

    return factory

def build_selector_resolver_factory(
    provider: ProviderResolver[Any, Any],
) -> ResolverFactory:

    def factory() -> SelectorResolver:
        return SelectorResolver(
            pipeline=provider.resolve(
                PipelineExecutor,
            ),
        )

    return factory

def build_template_value_resolver_factory(
    provider: ProviderResolver[Any, Any],
) -> ResolverFactory:

    def factory() -> TemplateValueResolver:
        return TemplateValueResolver(
            manager=provider.resolve(
                DefaultTemplateManager,
            ),
        )

    return factory

