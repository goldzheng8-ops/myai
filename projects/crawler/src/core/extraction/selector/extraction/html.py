from core.extraction.selector.extraction.mode import ExtractMode
from core.extraction.selector.extraction.base import ExtractionStrategy
from models.config.selector.base import SelectorConfig
from core.request.response.node import NodeAdapter


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