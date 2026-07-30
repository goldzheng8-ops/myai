from typing import Any, Sequence

from config.selector.base import SelectorConfig
from core.pipeline.extraction.registry import ExtractionRegistry
from core.pipeline.selection.registry import SelectionRegistry
from response.node import NodeAdapter

from .executor import PipelineExecutor


class Pipeline(PipelineExecutor):

    def __init__(
        self,
        selections: SelectionRegistry,
        extractions: ExtractionRegistry,
    ) -> None:

        self._get_selection = selections.create
        self._get_extraction = extractions.create

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