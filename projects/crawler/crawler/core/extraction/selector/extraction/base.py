

from abc import ABC, abstractmethod
from typing import Any

from core.extraction.selector.config import SelectorConfig
from core.plugin.base import Plugin
from core.extraction.response.node import NodeAdapter


class ExtractionStrategy(
    Plugin,
    ABC,
):

    @abstractmethod
    async def extract(
        self,
        node: NodeAdapter,
        selector: SelectorConfig,
    ) -> Any:
        ...