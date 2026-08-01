from typing import Any, Sequence

from models.config.selector.base import SelectorConfig
from core.pipeline.selection.mode import SelectionMode
from core.pipeline.selection.base import SelectionStrategy
from models.runtime.response.node import NodeAdapter
from ..extraction.base import ExtractionStrategy


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