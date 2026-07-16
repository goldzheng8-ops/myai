

from typing import Any

from adapters.base import ResponseAdapter
from config.config import SelectorConfig
from selector.base import SelectorPlugin


class RegexSelector(SelectorPlugin):
    name = "regex"

    def select(
        self,
        adapter: ResponseAdapter,
        selector: SelectorConfig
    ) -> Any:
        return adapter.select(selector)