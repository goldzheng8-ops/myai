

from typing import Any

from adapters.base import ResponseAdapter
from config.config import SelectorConfig
from selector.base import SelectorPlugin


class XPathSelector(SelectorPlugin):
    name = "xpath"

    def select(self, adapter: ResponseAdapter, selector: SelectorConfig) -> Any:
        return adapter.select(selector)
    


class XPathPlugin(SelectorPlugin):

    def select(self, adapter: ResponseAdapter, selector: SelectorConfig):
        return adapter.xpath(
            selector.query,
            many=selector.many,
        )