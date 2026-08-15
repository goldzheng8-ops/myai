from core.typing.config import BaseConfig
from core.extraction.selector.selection.mode import SelectionMode
from core.extraction.selector.extraction.mode import ExtractMode
from core.extraction.selector.typing import SelectorType



class SelectorConfig(BaseConfig):
    type: SelectorType
    selector: str
    selection: SelectionMode = SelectionMode.SINGLE
    extract: ExtractMode = ExtractMode.TEXT
    attribute: str | None = None

class CssSelectorConfig(SelectorConfig):
    type: SelectorType = SelectorType.CSS

class JmesPathSelectorConfig(SelectorConfig):
    type: SelectorType = SelectorType.JMESPATH

class JsonPathSelectorConfig(SelectorConfig):
    type: SelectorType = SelectorType.JSONPATH

class RegexSelectorConfig(SelectorConfig):
    type: SelectorType = SelectorType.REGEX
    flags: int = 0

class XpathSelectorConfig(SelectorConfig):
    type: SelectorType = SelectorType.XPATH
    selector: str