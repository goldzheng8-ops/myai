from core.pipeline.extraction.mode import ExtractMode
from core.pipeline.extraction.base import ExtractionStrategy
from config.selector.base import SelectorConfig
from response.node import NodeAdapter



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