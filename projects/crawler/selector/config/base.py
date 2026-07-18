


from core.models.base import BaseConfig
from selector.config.enums import SelectorType



class SelectorConfig(BaseConfig):
    type: SelectorType
    selector: str

    many: bool = False

    attribute: str | None = None