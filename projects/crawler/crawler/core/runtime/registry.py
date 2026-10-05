from typing import Any, Callable

from core.registry.base import Registry
from core.runtime.expression import ResolveExpression
from core.runtime.strategy.base import ResolveStrategy

ResolveStrategyFactory = Callable[
    [],
    ResolveStrategy[Any],
]


class ResolveRegistry(
    Registry[
        type[ResolveExpression],
        ResolveStrategyFactory,
    ],
):
    def create(
        self,
        expression_type: type[ResolveExpression],
    ) -> ResolveStrategy[Any]:

        factory = self.get(
            expression_type,
        )

        return factory()