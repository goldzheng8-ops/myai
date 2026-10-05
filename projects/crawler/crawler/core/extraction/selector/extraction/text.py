from core.extraction.selector.extraction.mode import ExtractMode
from core.extraction.selector.extraction.base import ExtractionStrategy
from core.extraction.selector.config import SelectorConfig
from core.extraction.response.node import NodeAdapter



class TextExtractionStrategy(
    ExtractionStrategy,
):

    plugin_type = ExtractMode.TEXT

    async def extract(
        self,
        node: NodeAdapter,
        selector: SelectorConfig,
    ) -> str | None:

        return await node.text()