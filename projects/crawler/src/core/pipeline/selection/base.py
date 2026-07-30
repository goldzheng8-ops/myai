from abc import ABC
from abc import abstractmethod
from typing import Sequence
from typing import Any

from config.selector.base import SelectorConfig
from response.node import NodeAdapter

from core.plugin.base import Plugin

from ..extraction.base import ExtractionStrategy


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