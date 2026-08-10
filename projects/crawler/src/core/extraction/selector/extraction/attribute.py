from typing import Any

from core.extraction.selector.extraction.base import ExtractionStrategy
from models.config.selector.base import SelectorConfig
from core.request.response.node import NodeAdapter

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