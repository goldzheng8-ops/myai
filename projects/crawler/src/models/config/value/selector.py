
from models.config.selector.base import SelectorConfig
from models.config.value.base import ValueConfig
from models.enums.value_type import ValueType


class SelectorValueConfig(ValueConfig):

    type: ValueType = ValueType.SELECTOR

    selector: SelectorConfig