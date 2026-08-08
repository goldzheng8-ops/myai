from abc import ABC
from abc import abstractmethod
from typing import Sequence
from typing import Any

from models.config.selector.base import SelectorConfig
from core.response.node import NodeAdapter

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