from typing import Any

from core.context.runtime_context import RuntimeContext
from core.expression.base import ExpressionEvaluator

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
        context: RuntimeContext,
    ) -> Any:

        return eval(
            expression,
            {},
            context.as_mapping(),
        )