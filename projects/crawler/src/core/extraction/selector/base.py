from typing import Any, Sequence

from models.config.selector.base import SelectorConfig
from core.extraction.selector.extraction.registry import ExtractionRegistry
from core.extraction.selector.selection.registry import SelectionRegistry
from core.request.response.node import NodeAdapter

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