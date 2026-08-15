from typing import Any, Sequence

from core.extraction.selector.config import SelectorConfig
from core.extraction.selector.selection.mode import SelectionMode
from core.extraction.selector.selection.base import SelectionStrategy
from core.extraction.response.node import NodeAdapter
from core.extraction.selector.extraction.base import ExtractionStrategy


class MultipleSelectionStrategy(
    SelectionStrategy,
):

    plugin_type = SelectionMode.MULTIPLE

    async def select(
        self,
        nodes: Sequence[NodeAdapter],
        extraction: ExtractionStrategy,
        selector: SelectorConfig,
    ) -> Any:

        return [
            await extraction.extract(
                node,
                selector,
            )
            for node in nodes
        ]