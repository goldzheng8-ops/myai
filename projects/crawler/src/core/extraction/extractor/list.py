from typing import Any



from core.extraction.extractor.base import Extractor
from core.extraction.extractor.config import ListConfig
from core.extraction.extractor.executor import ExtractExecutor
from core.extraction.extractor.context import ExtractContext
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
    ) -> list[Any]:


        nodes = await context.response.select_nodes(
            config.selector,
        )


        result = []


        for node in nodes:


            child_context = context.with_node(
                node,
            )


            value = await self._executor.extract(
                config.item,
                child_context,
            )


            result.append(
                value
            )


        return result