

from config.value.base import ValueConfig
from enums.value_type import ValueType

class ExpressionValueConfig(ValueConfig):

    type: ValueType = ValueType.EXPRESSION

    expression: str