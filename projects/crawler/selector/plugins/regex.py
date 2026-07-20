from adapters.base import ResponseAdapter
from config.config import SelectorConfig
from selector.base import SelectorPlugin
from selector.config.enums import SelectorType


class RegexSelector(SelectorPlugin):
    type=SelectorType.REGEX

    def select(
        self,
        adapter: ResponseAdapter,
        selector: SelectorConfig
    ):
        return adapter.regex(selector)