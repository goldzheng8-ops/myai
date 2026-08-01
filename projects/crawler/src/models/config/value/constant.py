from typing import Any

from models.config.value.base import ValueConfig
from models.enums.value_type import ValueType

class ConstantValueConfig(ValueConfig):

    type: ValueType = ValueType.CONSTANT

    value: Any