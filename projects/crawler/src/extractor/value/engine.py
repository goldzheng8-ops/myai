

from adapters.base import ResponseAdapter
from config.value.base import ValueConfig
from extractor.value.registry import ValueRegistry
from scope.object.builder import ObjectContextBuilder
from core.context.extract_context import ExtractContext


class ValueEngine:

    def __init__(
        self,
        registry: ValueRegistry,
        scope_builder: ObjectContextBuilder,
    ) -> None:

        self._registry = registry

        self._scope_builder = scope_builder

    async def extract(

        self,

        *,

        response:ResponseAdapter,

        context:ExtractContext,

        config:ValueConfig,

    ):

        object_context = self._scope_builder.build(
            context,
        )

        plugin = self._registry.create(
            config.type,
        )

        return await plugin.extract(

            response=response,

            context=context,

            object_context=object_context,

            config=config,

        )