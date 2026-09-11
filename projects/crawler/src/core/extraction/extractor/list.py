from typing import Any



from core.extraction.extractor.base import Extractor
from core.extraction.extractor.config import ListConfig
from core.extraction.extractor.executor import ExtractExecutor
from core.extraction.extractor.context import ExtractContext
from core.extraction.extractor.result import ExtractResult
from core.extraction.extractor.typing import ExtractType

class ListExtractor(
    Extractor[ListConfig],
):

    plugin_type = ExtractType.LIST


    def __init__(
        self,
        executor: ExtractExecutor,
    ):
        self._executor = executor

    async def extract(
        self,
        config: ListConfig,
        context: ExtractContext,
    ) -> ExtractResult:


        nodes = await context.response.select_nodes(
            config.selector,
        )


        items: list[Any] = []


        for node in nodes:


            child_context = context.with_node(
                node,
            )


            result = await self._executor.extract(
                config.item,
                child_context,
            )


            items.append(result.data)

        return ExtractResult(
            data=items,
            metadata=config.metadata.copy(),
        )