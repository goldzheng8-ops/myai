

from config.extractor.base import ExtractConfig
from config.selector.base import SelectorConfig
from enums.extract_type import ExtractType

class ListConfig(ExtractConfig):

    type = ExtractType.LIST

    selector: SelectorConfig

    item: ExtractConfig

