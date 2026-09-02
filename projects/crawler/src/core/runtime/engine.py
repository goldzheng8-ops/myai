from typing import TYPE_CHECKING, Any

from core.runtime.expression import ResolveExpression
from core.runtime.registry import ResolveRegistry

if TYPE_CHECKING:
    from core.runtime.context import RuntimeContext
else:
    RuntimeContext = Any


class ResolveEngine:

    def __init__(
        self,
        registry: ResolveRegistry,
    ):

        self._registry = registry

    def resolve(
        self,
        context: RuntimeContext,
        expression: ResolveExpression,
    ):

        strategy = self._registry.get(
            type(expression)
        )

        return strategy.resolve(
            context,
            expression,
        )