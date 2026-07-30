from typing import Any, Sequence

from config.selector.base import SelectorConfig
from core.pipeline.selection.mode import SelectionMode
from core.pipeline.selection.base import SelectionStrategy
from response.node import NodeAdapter
from ..extraction.base import ExtractionStrategy

class SingleSelectionStrategy(
    SelectionStrategy,
):

    plugin_type = SelectionMode.SINGLE

    async def select(
        self,
        nodes: Sequence[NodeAdapter],
        extraction: ExtractionStrategy,
        selector: SelectorConfig,
    ) -> Any:

        if not nodes:
            return None

        return await extraction.extract(
            nodes[0],
            selector,
        )