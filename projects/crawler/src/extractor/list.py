from typing import Any


from config.extractor.list import ListConfig
from enums.extract_type import ExtractType
from extractor.base import Extractor
from extractor.executor import ExtractExecutor
from core.context.extract_context import ExtractContext

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