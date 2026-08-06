from typing import Any

from core.registry.base import Registry
from core.runtime.expression import ResolveExpression
from core.runtime.strategy import ResolveStrategy
class ResolveRegistry(
    Registry[
        type[
            ResolveExpression
        ],
        ResolveStrategy[Any],
    ]
):
    pass