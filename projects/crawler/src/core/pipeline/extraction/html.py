from core.pipeline.extraction.mode import ExtractMode
from core.pipeline.extraction.base import ExtractionStrategy
from models.config.selector.base import SelectorConfig
from models.runtime.response.node import NodeAdapter


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