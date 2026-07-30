

from typing import Any

from adapters.base import ResponseAdapter
from config.value.selector import SelectorValueConfig
from enums.value_type import ValueType
from extractor.value.base import ValuePlugin
from core.context.runtime_context import ObjectContext
from core.context.extract_context import ExtractContext


class SelectorValuePlugin(

    ValuePlugin[
        SelectorValueConfig
    ]

):

    plugin_type = ValueType.SELECTOR

    config_type = SelectorValueConfig

    async def extract(
        self,
        *,
        response: ResponseAdapter,
        context: ExtractContext,
        object_context: ObjectContext,
        config: SelectorValueConfig,
    ) -> Any:

        return await response.select(
            config.selector,
        )