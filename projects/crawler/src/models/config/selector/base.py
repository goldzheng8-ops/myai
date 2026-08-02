from models.config.base import BaseConfig
from selector.selection.mode import SelectionMode
from selector.extraction.mode import ExtractMode
from models.enums.selector_type import SelectorType



class SelectorConfig(BaseConfig):

    type: SelectorType

    selector: str

    selection: SelectionMode = SelectionMode.SINGLE

    extract: ExtractMode = ExtractMode.TEXT

    attribute: str | None = None