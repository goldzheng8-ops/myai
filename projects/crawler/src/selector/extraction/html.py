from selector.extraction.mode import ExtractMode
from selector.extraction.base import ExtractionStrategy
from models.config.selector.base import SelectorConfig
from core.response.node import NodeAdapter


class HtmlExtractionStrategy(
    ExtractionStrategy,
):

    plugin_type = ExtractMode.HTML

    async def extract(
        self,
        node: NodeAdapter,
        selector: SelectorConfig,
    ) -> str:

        return await node.html()