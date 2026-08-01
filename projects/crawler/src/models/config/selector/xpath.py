from models.config.selector.base import SelectorConfig
from models.enums.selector_type import SelectorType



class XpathSelectorConfig(SelectorConfig):
    type: SelectorType = SelectorType.XPATH

    selector: str