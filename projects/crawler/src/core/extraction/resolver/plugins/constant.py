from typing import Any

from models.config.value.constant import ConstantValueConfig
from core.extraction.extractor.context import ExtractContext
from models.enums.value_type import ValueType
from core.extraction.resolver.base import Resolver



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