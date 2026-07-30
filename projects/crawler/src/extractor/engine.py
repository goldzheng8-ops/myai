from config.extractor.base import ExtractConfig

from .executor import ExtractExecutor
from .registry import ExtractorRegistry
from core.context.extract_context import ExtractContext


class ExtractEngine(

    ExtractExecutor,

):

    def __init__(

        self,

        registry: ExtractorRegistry,

    ):

        self._registry = registry

    async def execute(

        self,

        config: ExtractConfig,

        context: ExtractContext,

    ):

        extractor = self._registry.create(
            config.type,
        )

        return await extractor.extract(
            config,
            context,
            self,
        )