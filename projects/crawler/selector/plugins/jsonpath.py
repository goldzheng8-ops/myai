

from typing import Any

from adapters.base import ResponseAdapter
from config.config import SelectorConfig
from selector.base import SelectorPlugin
from selector.config.enums import SelectorType



class JsonPathSelector(SelectorPlugin):
    type=SelectorType.JSONPATH

    def select(self, adapter: ResponseAdapter, selector: SelectorConfig) -> Any:
        # Implement JSONPath selection logic here
        return adapter.jsonpath(selector)