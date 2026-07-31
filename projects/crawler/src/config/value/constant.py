from typing import Any

from config.value.base import ValueConfig
from enums.value_type import ValueType

class ConstantValueConfig(ValueConfig):

    type: ValueType = ValueType.CONSTANT

    value: Any