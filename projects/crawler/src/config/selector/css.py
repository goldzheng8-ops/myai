from config.selector.base import SelectorConfig
from enums.selector_type import SelectorType


class CssSelectorConfig(SelectorConfig):
    type: SelectorType = SelectorType.CSS

