from typing import Annotated, Literal

from core.typing.config import BaseConfig
from core.extraction.selector.selection.mode import SelectionMode
from core.extraction.selector.extraction.mode import ExtractMode
from core.extraction.selector.typing import SelectorType
from pydantic import Field



class SelectorConfig(BaseConfig):
    selector: str
    selection: SelectionMode = SelectionMode.SINGLE
    extract: ExtractMode = ExtractMode.TEXT
    attribute: str | None = None


class CssSelectorConfig(SelectorConfig):
    type: Literal[SelectorType.CSS] = SelectorType.CSS


class JmesPathSelectorConfig(SelectorConfig):
    type: Literal[SelectorType.JMESPATH] = SelectorType.JMESPATH


class JsonPathSelectorConfig(SelectorConfig):
    type: Literal[SelectorType.JSONPATH] = SelectorType.JSONPATH


class RegexSelectorConfig(SelectorConfig):
    type: Literal[SelectorType.REGEX] = SelectorType.REGEX
    flags: int = 0


class XpathSelectorConfig(SelectorConfig):
    type: Literal[SelectorType.XPATH] = SelectorType.XPATH

SelectorConfigUnion = Annotated[
    (
        CssSelectorConfig
        | JmesPathSelectorConfig
        | JsonPathSelectorConfig
        | RegexSelectorConfig
        | XpathSelectorConfig
    ),
    Field(discriminator="type"),
]