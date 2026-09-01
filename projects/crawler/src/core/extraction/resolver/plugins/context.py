from typing import Any

from core.extraction.value.config import ContextValueConfig
from core.extraction.extractor.context import ExtractContext
from core.extraction.value.typing import ValueType
from core.extraction.resolver.base import Resolver


class ContextResolver(
    Resolver[ContextValueConfig],
):

    plugin_type = ValueType.CONTEXT


    async def resolve(
        self,
        config: ContextValueConfig,
        context:ExtractContext,
    ) -> Any:

        return config.key
        