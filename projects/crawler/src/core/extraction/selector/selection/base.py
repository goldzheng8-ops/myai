from abc import ABC
from abc import abstractmethod
from collections.abc import Sequence
from typing import Any

from core.extraction.selector.config import SelectorConfig
from core.extraction.response.node import NodeAdapter
from core.plugin.base import Plugin
from core.extraction.selector.extraction.base import ExtractionStrategy


class SelectionStrategy(
    Plugin,
    ABC,
):

    @abstractmethod
    async def select(
        self,
        nodes: Sequence[NodeAdapter],
        extraction: ExtractionStrategy,
        selector: SelectorConfig,
    ) -> Any:
        ...