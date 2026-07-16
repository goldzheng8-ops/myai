from typing import Any

from adapters.base import ResponseAdapter
from config.config import SelectorConfig
from selector.registry import registry as selector_registry



class SelectorEngine:

    def __init__(self):
        self.registry = selector_registry

    def select(
        self,
        adapter: ResponseAdapter,
        selector: SelectorConfig,
    ) -> Any:

        plugin = self.registry.get(selector.type)

        return plugin.select(adapter, selector)