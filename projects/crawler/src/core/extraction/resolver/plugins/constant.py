from typing import Any
from core.extraction.value.typing import ValueType
from core.extraction.value.config import ConstantValueConfig
from core.extraction.extractor.context import ExtractContext
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