
from config.value.base import ValueConfig
from enums.value_type import ValueType

class ContextValueConfig(ValueConfig):

    type = ValueType.CONTEXT

    key: str