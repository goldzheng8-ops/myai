

from typing import Any

from adapters.base import ResponseAdapter

from config.value.constant import ConstantValueConfig
from enums.value_type import ValueType
from extractor.value.base import ValuePlugin
from core.context.runtime_context import ObjectContext
from core.context.extract_context import ExtractContext

class ConstantValuePlugin(

    ValuePlugin[
        ConstantValueConfig
    ]

):

    plugin_type = ValueType.CONSTANT

    config_type = ConstantValueConfig

    async def extract(
        self,
        *,
        response: ResponseAdapter,
        context: ExtractContext,
        object_context: ObjectContext,
        config: ConstantValueConfig,
    ) -> Any:

        return config.value