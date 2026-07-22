from config.selector.base import SelectorConfig
from enums.selector_type import SelectorType


class RegexSelectorConfig(SelectorConfig):
    type: SelectorType = SelectorType.REGEX

    flags: int = 0