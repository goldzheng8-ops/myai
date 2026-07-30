from core.pipeline.extraction.base import ExtractionStrategy
from core.pipeline.extraction.mode import ExtractMode
from config.selector.base import SelectorConfig
from response.node import NodeAdapter

class AttributeExtractionStrategy(
    ExtractionStrategy,
):

    plugin_type = ExtractMode.ATTRIBUTE

    async def extract(
        self,
        node: NodeAdapter,
        selector: SelectorConfig,
    ) -> str | None:

        return await node.attribute(
            selector.attribute,
        )