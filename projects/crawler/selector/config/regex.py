

from selector.config.base import SelectorConfig, SelectorType


class RegexSelectorConfig(SelectorConfig):
    type: SelectorType = SelectorType.REGEX

    flags: int = 0