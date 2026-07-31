

from config.value.base import ValueConfig
from enums.value_type import ValueType

class TemplateValueConfig(ValueConfig):

    type: ValueType = ValueType.TEMPLATE

    template: str