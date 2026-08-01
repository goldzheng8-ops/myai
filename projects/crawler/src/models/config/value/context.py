
from models.config.value.base import ValueConfig
from models.enums.value_type import ValueType

class ContextValueConfig(ValueConfig):

    type: ValueType = ValueType.CONTEXT

    key: str