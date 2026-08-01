from abc import ABC, abstractmethod
from typing import Any

from models.runtime.extract.runtime import RuntimeContext

class ExpressionEvaluator(ABC):

    @abstractmethod
    def evaluate(
        self,
        expression: str,
        context: RuntimeContext,
    ) -> Any:
        ...