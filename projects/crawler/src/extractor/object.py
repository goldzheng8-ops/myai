from typing import Any

from config.extractor.object import ObjectConfig
from enums.extract_type import ExtractType
from extractor.base import Extractor

from core.context.extract_context import ExtractContext
from extractor.executor import ExtractExecutor

class ObjectExtractor(
    Extractor[ObjectConfig],
):

    plugin_type = ExtractType.OBJECT


    def __init__(
        self,
        executor: ExtractExecutor,
    ):
        self._executor = executor

    async def extract(
        self,
        config: ObjectConfig,
        context: ExtractContext,
    ) -> dict[str, Any]:

        result = {}
        for child in config.children:
            value = await self._executor.extract(
                child,
                context,
            )
            result[child.name] = value
        return result