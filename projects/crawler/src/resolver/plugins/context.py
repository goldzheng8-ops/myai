from typing import Any

from models.config.value.context import ContextValueConfig
from models.runtime.extract.context import ExtractContext
from models.enums.value_type import ValueType
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