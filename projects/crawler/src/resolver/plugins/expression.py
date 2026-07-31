
from config.value.expression import ExpressionValueConfig
from core.context.extract_context import ExtractContext

from core.expression.default import DefaultExpressionEvaluator
from enums.value_type import ValueType
from resolver.base import Resolver


class ExpressionResolver(
    Resolver[ExpressionValueConfig],
):

    plugin_type = ValueType.EXPRESSION


    def __init__(
        self,
        evaluator:DefaultExpressionEvaluator,
    ):
        self._evaluator = evaluator


    async def resolve(
        self,
        config:ExpressionValueConfig,
        context:ExtractContext,
    ):

        return self._evaluator.evaluate(
            config.expression,
            context.runtime,
        )