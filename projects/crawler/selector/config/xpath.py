


from selector.config.base import SelectorConfig, SelectorType


class XpathSelectorConfig(SelectorConfig):
    type: SelectorType = SelectorType.XPATH

    selector: str