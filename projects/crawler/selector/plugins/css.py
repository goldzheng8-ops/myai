

from adapters.base import ResponseAdapter
from config.config import SelectorConfig
from selector.base import SelectorPlugin


class CssSelector(SelectorPlugin):
    name = "css"

    def select(self, adapter: ResponseAdapter, selector: SelectorConfig, **kwargs):
        return adapter.select(selector)