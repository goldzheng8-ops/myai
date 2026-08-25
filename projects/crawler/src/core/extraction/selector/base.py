from typing import Any, Sequence

from core.extraction.selector.config import SelectorConfig
from core.extraction.selector.extraction.registry import ExtractionRegistry
from core.extraction.selector.selection.registry import SelectionRegistry
from core.extraction.response.node import NodeAdapter

from core.extraction.selector.executor import PipelineExecutor


class SelectorPipeline(PipelineExecutor):

    def __init__(
        self,
        selections: SelectionRegistry,
        extractions: ExtractionRegistry,
    ) -> None:

        self._get_selection = selections.get
        self._get_extraction = extractions.get

    async def execute(
        self,
        nodes: Sequence[NodeAdapter],
        selector: SelectorConfig,
    ) -> Any:

        selection = self._get_selection(
            selector.selection,
        )

        extraction = self._get_extraction(
            selector.extract,
        )

        return await selection.select(
            nodes,
            extraction,
            selector,
        )