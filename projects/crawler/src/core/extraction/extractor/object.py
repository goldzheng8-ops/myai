from typing import Any

import logging
from core.extraction.exception import RequiredFieldMissingError
from core.extraction.extractor.base import Extractor

from core.extraction.extractor.config import ObjectConfig
from core.extraction.extractor.context import ExtractContext
from core.extraction.extractor.executor import ExtractExecutor
from core.extraction.extractor.result import ExtractResult
from core.extraction.extractor.typing import ExtractType

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
    ) -> ExtractResult:

        data: dict[str, Any] = {}
        for child in config.children:
            try:
                result = await self._executor.extract(
                    child,
                    context,
                )
            except RequiredFieldMissingError as exc:
                logger = logging.getLogger(__name__)

                logger.warning(
                    "Discard incomplete item: %s",
                    exc,
                )
                continue            
            data[child.name] = result.data
        return ExtractResult(
            data=data,
            metadata=config.metadata.copy(),
        )