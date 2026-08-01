from models.config.base import BaseConfig
from core.pipeline.selection.mode import SelectionMode
from core.pipeline.extraction.mode import ExtractMode
from models.enums.selector_type import SelectorType



class SelectorConfig(BaseConfig):

    type: SelectorType

    selector: str

    selection: SelectionMode = SelectionMode.SINGLE

    extract: ExtractMode = ExtractMode.TEXT

    attribute: str | None = None