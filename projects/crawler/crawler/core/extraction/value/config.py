from typing import Annotated, Any, Literal

from core.typing.config import BaseConfig
from core.extraction.value.typing import ValueType
from core.extraction.selector.config import SelectorConfigUnion
from pydantic import Field

class ConstantValueConfig(BaseConfig):
    type: Literal[ValueType.CONSTANT] = ValueType.CONSTANT
    value: Any


class ContextValueConfig(BaseConfig):
    type: Literal[ValueType.CONTEXT] = ValueType.CONTEXT
    key: str


class ExpressionValueConfig(BaseConfig):
    type: Literal[ValueType.EXPRESSION] = ValueType.EXPRESSION
    expression: str


class SelectorValueConfig(BaseConfig):
    type: Literal[ValueType.SELECTOR] = ValueType.SELECTOR
    selector: SelectorConfigUnion


class TemplateValueConfig(BaseConfig):
    type: Literal[ValueType.TEMPLATE] = ValueType.TEMPLATE
    template: str

ValueConfigUnion = Annotated[
    (
        ConstantValueConfig
        | ContextValueConfig
        | ExpressionValueConfig
        | SelectorValueConfig
        | TemplateValueConfig
    ),
    Field(discriminator="type"),
]