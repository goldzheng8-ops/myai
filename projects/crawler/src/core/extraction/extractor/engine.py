from typing import Any

from .config import ExtractConfig

from .executor import ExtractExecutor
from .registry import ExtractorRegistry
from core.extraction.extractor.context import ExtractContext


class ExtractEngine(

    ExtractExecutor,

):

    def __init__(
        self,
        registry: ExtractorRegistry,
    ):
        self._registry = registry


    async def extract(
        self,
        config: ExtractConfig,
        context: ExtractContext,
    ) -> Any:


        extractor = self._registry.create(
            config.type,
        )


        return await extractor.extract(
            config,
            context,
        )