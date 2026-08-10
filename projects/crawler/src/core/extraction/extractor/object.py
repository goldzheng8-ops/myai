from typing import Any

from models.config.extractor.object import ObjectConfig
from models.enums.extract_type import ExtractType
from core.extraction.extractor.base import Extractor

from models.runtime.extract.context import ExtractContext
from core.extraction.extractor.executor import ExtractExecutor

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