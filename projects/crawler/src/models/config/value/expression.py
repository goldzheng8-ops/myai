

from models.config.value.base import ValueConfig
from models.enums.value_type import ValueType

class ExpressionValueConfig(ValueConfig):

    type: ValueType = ValueType.EXPRESSION

    expression: str