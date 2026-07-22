from typing import Literal

from core.models.base import BaseConfig
from enums.selector_type import SelectorType



class SelectorConfig(BaseConfig):
    type: SelectorType
    selector: str

    many: bool = False
    extract: Literal["text", "html"] | None = "text"
    attribute: str | None = None