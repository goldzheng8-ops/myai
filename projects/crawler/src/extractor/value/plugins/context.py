
from typing import Any

from adapters.base import ResponseAdapter


from config.value.context import ContextValueConfig
from enums.value_type import ValueType
from extractor.value.base import ValuePlugin
from core.context.runtime_context import ObjectContext
from core.context.extract_context import ExtractContext

class ContextValuePlugin(

    ValuePlugin[
        ContextValueConfig
    ]

):

    plugin_type = ValueType.CONTEXT

    config_type = ContextValueConfig

    async def extract(
        self,
        *,
        response: ResponseAdapter,
        context: ExtractContext,
        object_context: ObjectContext,
        config: ContextValueConfig,
    ) -> Any:

        return object_context.resolve(
            config.key,
        )