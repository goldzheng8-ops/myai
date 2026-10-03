from typing import Any

from core.cache.protocol import Cache
from core.provider.protocol import ProviderResolver
from core.provider.builder import ProviderBuilder
from core.provider.factory import FactoryProvider
from core.runtime import RuntimeContext
from core.runtime.engine import ResolveEngine
from core.runtime.expression import DotPathExpression, TemplateExpression
from core.runtime.registry import ResolveRegistry
from core.runtime.strategy.dot_path import DotPathStrategy
from core.runtime.strategy.template import TemplateStrategy

def register_runtime_context(
    builder: ProviderBuilder,
) -> None:


    builder.add_factory(
        RuntimeContext,
        lambda resolver: RuntimeContext(
            _resolve_engine=resolver.resolve(
                ResolveEngine,
            ),
            _cache=resolver.resolve(
                Cache,
            ),

        ),
        strategy_cls=FactoryProvider,
    )
    builder.add_factory(
        ResolveEngine,
        lambda resolver: ResolveEngine(
            registry=resolver.resolve(
                ResolveRegistry,
            ),
        ),
    )
    builder.add_factory(
        ResolveRegistry,
        lambda resolver: create_resolve_registry(
            resolver=resolver,
        ),
    )

def create_resolve_registry(
    *,
    resolver: ProviderResolver[Any, Any],
) -> ResolveRegistry:

    registry = ResolveRegistry()

    registry.register(
        DotPathExpression,
        lambda : resolver.resolve(
            DotPathStrategy,
        ),
    )
    registry.register(
        TemplateExpression,
        lambda : resolver.resolve(
            TemplateStrategy,
        ),
    )



    return registry