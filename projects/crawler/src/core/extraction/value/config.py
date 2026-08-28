from typing import Annotated, Any, Literal

from core.typing.config import BaseConfig
from core.extraction.value.typing import ValueType
from core.extraction.selector.config import SelectorConfig, SelectorConfigUnion
from pydantic import Field

class ValueConfig(BaseConfig):
    type: ValueType


class ConstantValueConfig(ValueConfig):
    type: Literal[ValueType.CONSTANT] = ValueType.CONSTANT
    value: Any


class ContextValueConfig(ValueConfig):
    type: Literal[ValueType.CONTEXT] = ValueType.CONTEXT
    key: str


class ExpressionValueConfig(ValueConfig):
    type: Literal[ValueType.EXPRESSION] = ValueType.EXPRESSION
    expression: str


class SelectorValueConfig(ValueConfig):
    type: Literal[ValueType.SELECTOR] = ValueType.SELECTOR
    selector: SelectorConfigUnion


class TemplateValueConfig(ValueConfig):
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