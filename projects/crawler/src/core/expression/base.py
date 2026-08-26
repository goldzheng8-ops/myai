from abc import ABC, abstractmethod
from typing import Any

from core.runtime import RuntimeContext

class ExpressionEvaluator(ABC):

    @abstractmethod
    def evaluate(
        self,
        expression: str,
        context: RuntimeContext,
    ) -> Any:
        ...