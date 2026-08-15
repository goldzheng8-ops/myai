from typing import Any

from core.typing.config import BaseConfig
from core.extraction.value.typing import ValueType
from core.extraction.selector.config import SelectorConfig

class ValueConfig(BaseConfig):

    type: ValueType

class ConstantValueConfig(ValueConfig):

    type: ValueType = ValueType.CONSTANT

    value: Any

class ContextValueConfig(ValueConfig):

    type: ValueType = ValueType.CONTEXT

    key: str

class ExpressionValueConfig(ValueConfig):

    type: ValueType = ValueType.EXPRESSION

    expression: str

class SelectorValueConfig(ValueConfig):

    type: ValueType = ValueType.SELECTOR

    selector: SelectorConfig

class TemplateValueConfig(ValueConfig):

    type: ValueType = ValueType.TEMPLATE

    template: str