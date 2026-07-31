
from config.selector.base import SelectorConfig
from config.value.base import ValueConfig
from enums.value_type import ValueType


class SelectorValueConfig(ValueConfig):

    type: ValueType = ValueType.SELECTOR

    selector: SelectorConfig