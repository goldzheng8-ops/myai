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
    config_type = ListConfig

    def __init__(
        self,
        executor: ExtractExecutor,
    ) -> None:
        self._executor = executor

    async def extract(
        self,
        config: ListConfig,
        context: ExtractContext,
    ) -> list[Any]:

        parent = (
            context.current
            if context.current is not None
            else context.response
        )

        nodes = await parent.select(
            config.selector,
        )

        result: list[Any] = []

        for node in nodes:

            child_context = context.with_current(
                node,
            )

            result.append(
                await self._executor.extract(
                    config.item,
                    child_context,
                )
            )

        return result