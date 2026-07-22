from config.selector.base import SelectorConfig
from enums.selector_type import SelectorType



class XpathSelectorConfig(SelectorConfig):
    type: SelectorType = SelectorType.XPATH

    selector: str