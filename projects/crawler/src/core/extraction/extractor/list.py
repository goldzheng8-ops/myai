from typing import Any


from models.config.extractor.list import ListConfig
from models.enums.extract_type import ExtractType
from core.extraction.extractor.base import Extractor
from core.extraction.extractor.executor import ExtractExecutor
from models.runtime.extract.context import ExtractContext

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