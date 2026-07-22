from adapters.base import ResponseAdapter
from config.config import SelectorConfig
from selector.base import SelectorPlugin
from selector.config.enums import SelectorType


class CssSelectorPlugin(SelectorPlugin):

    type = SelectorType.CSS

    def css(self, adapter: ResponseAdapter, selector: SelectorConfig):
        # Implement JSONPath selection logic here
        return adapter.jsonpath(selector)