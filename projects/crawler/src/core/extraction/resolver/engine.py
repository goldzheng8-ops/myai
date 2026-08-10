from typing import Any

from models.config.value.base import ValueConfig
from models.runtime.extract.context import ExtractContext
from core.extraction.resolver.executor import ResolverExecutor
from core.extraction.resolver.registry import ResolverRegistry

class ResolverEngine(
    ResolverExecutor,
):

    def __init__(
        self,
        registry: ResolverRegistry,
    ):
        self._registry = registry


    async def resolve(
        self,
        config: ValueConfig,
        context: ExtractContext,
    ) -> Any:

        resolver = self._registry.create(
            config.type,
        )

        return await resolver.resolve(
            config,
            context,
        )