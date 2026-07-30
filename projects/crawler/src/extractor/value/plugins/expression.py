from adapters.base import ResponseAdapter


from config.value.expression import ExpressionValueConfig
from enums.value_type import ValueType
from extractor.value.base import ValuePlugin

from extractor.value.evaluator import ExpressionEvaluator
from core.context.runtime_context import ObjectContext
from core.context.extract_context import ExtractContext

class ExpressionValuePlugin(
    ValuePlugin[
        ExpressionValueConfig
    ],
):

    plugin_type = ValueType.EXPRESSION

    config_type = ExpressionValueConfig

    def __init__(
        self,
        evaluator: ExpressionEvaluator,
    ) -> None:

        self._evaluator = evaluator

    async def extract(
        self,
        *,
        response: ResponseAdapter,
        context: ExtractContext,
        object_context: ObjectContext,
        config: ExpressionValueConfig,
    ):

        return self._evaluator.evaluate(
            config.expression,
            object_context,
        )