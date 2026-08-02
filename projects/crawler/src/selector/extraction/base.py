

from abc import ABC, abstractmethod
from typing import Any

from models.config.selector.base import SelectorConfig
from core.plugin.base import Plugin
from models.runtime.response.node import NodeAdapter


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