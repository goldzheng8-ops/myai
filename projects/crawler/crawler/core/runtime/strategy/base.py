from abc import ABC, abstractmethod
from typing import Any, Generic

from core.runtime.context import RuntimeContext
from core.runtime.typing import ExpressionT

class ResolveStrategy(
    Generic[ExpressionT],
    ABC,
):

    @abstractmethod
    def resolve(
        self,
        context: RuntimeContext,
        expression: ExpressionT,
    ) -> Any:
        ...