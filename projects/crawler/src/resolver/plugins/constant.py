from typing import Any

from config.value.constant import ConstantValueConfig
from core.context.extract_context import ExtractContext
from enums.value_type import ValueType
from resolver.base import Resolver



class ConstantResolver(
    Resolver[ConstantValueConfig],
):

    plugin_type = ValueType.CONSTANT


    async def resolve(
        self,
        config: ConstantValueConfig,
        context:ExtractContext,
    ) -> Any:

        return config.value