
from models.config.value.expression import ExpressionValueConfig
from core.extraction.extractor.context import ExtractContext

from core.expression.default import DefaultExpressionEvaluator
from models.enums.value_type import ValueType
from core.extraction.resolver.base import Resolver


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