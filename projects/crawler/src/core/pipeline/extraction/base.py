

from abc import ABC, abstractmethod
from typing import Any

from config.selector.base import SelectorConfig
from core.plugin.base import Plugin
from response.node import NodeAdapter


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