from abc import ABC, abstractmethod
from typing import Any

from extractor.value.utils.object_context import ObjectContext


class ExpressionEvaluator(ABC):

    @abstractmethod
    def evaluate(
        self,
        expression: str,
        context: ObjectContext,
    ) -> Any:
        ...

class DefaultExpressionEvaluator(
    ExpressionEvaluator,
):


    '''
这个实现只建议开发阶段使用。

以后替换成：

simpleeval
asteval
CEL
JsonLogic
    '''
    def evaluate(
        self,
        expression: str,
        context: ObjectContext,
    ) -> Any:

        return eval(
            expression,
            {},
            context.as_mapping(),
        )