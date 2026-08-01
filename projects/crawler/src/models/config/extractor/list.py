

from models.config.extractor.base import ExtractConfig
from models.config.selector.base import SelectorConfig
from models.enums.extract_type import ExtractType

class ListConfig(ExtractConfig):

    type = ExtractType.LIST

    selector: SelectorConfig

    item: ExtractConfig

