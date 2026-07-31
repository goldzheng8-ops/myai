from typing import Any

from core.pipeline.extraction.base import ExtractionStrategy
from config.selector.base import SelectorConfig
from response.node import NodeAdapter

class AttributeExtractionStrategy(
    ExtractionStrategy,
):

    async def extract(
        self,
        node: NodeAdapter,
        selector: SelectorConfig,
    ) -> Any:

        attribute = selector.attribute

        if attribute is None:
            raise ValueError(
                "Attribute selector requires 'attribute'."
            )

        return await node.attribute(attribute)