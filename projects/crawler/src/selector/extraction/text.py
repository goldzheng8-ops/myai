from selector.extraction.mode import ExtractMode
from selector.extraction.base import ExtractionStrategy
from models.config.selector.base import SelectorConfig
from models.runtime.response.node import NodeAdapter



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