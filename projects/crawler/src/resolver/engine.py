from typing import Any

from config.value.base import ValueConfig
from core.context.extract_context import ExtractContext
from resolver.executor import ResolverExecutor
from resolver.registry import ResolverRegistry

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