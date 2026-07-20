from adapters.base import ResponseAdapter
from config.config import SelectorConfig
from selector.base import SelectorPlugin
from selector.config.enums import SelectorType


class XPathSelector(SelectorPlugin):
    type=SelectorType.XPATH

    def select(self, adapter: ResponseAdapter, selector: SelectorConfig):
        return adapter.xpath(selector)