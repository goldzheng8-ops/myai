from typing import Any

from config.value.context import ContextValueConfig
from core.context.extract_context import ExtractContext
from enums.value_type import ValueType
from resolver.base import Resolver


class ContextResolver(
    Resolver[ContextValueConfig],
):

    plugin_type = ValueType.CONTEXT


    async def resolve(
        self,
        config: ContextValueConfig,
        context:ExtractContext,
    ) -> Any:

        return context.runtime.resolve(
            config.key,
        )