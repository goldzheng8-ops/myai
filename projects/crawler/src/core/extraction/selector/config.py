from typing import Annotated, Literal, Self

from core.typing.config import BaseConfig
from core.extraction.selector.selection.mode import SelectionMode
from core.extraction.selector.extraction.mode import ExtractMode
from core.extraction.selector.typing import SelectorType
from pydantic import Field, model_validator



class SelectorConfig(BaseConfig):
    selector: str
    selection: SelectionMode = SelectionMode.SINGLE
    extract: ExtractMode = ExtractMode.TEXT
    attribute: str | None = None
    @model_validator(mode="after")
    def validate_attribute(self) -> Self:
        if (
            self.extract == ExtractMode.ATTRIBUTE
            and self.attribute is None
        ):
            raise ValueError(
                "attribute is required when "
                "extract mode is 'attribute'."
            )

        if (
            self.extract != ExtractMode.ATTRIBUTE
            and self.attribute is not None
        ):
            raise ValueError(
                "attribute is only valid when "
                "extract mode is 'attribute'."
            )

        return self


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