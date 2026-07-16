

from typing import Any

from adapters.base import ResponseAdapter
from config.config import SelectorConfig
from selector.base import SelectorPlugin


class JsonPathSelector(SelectorPlugin):
    name = "jsonpath"

    def select(self, adapter: ResponseAdapter, selector: SelectorConfig,) -> Any:
        # Implement JSONPath selection logic here
        return adapter.select(selector)