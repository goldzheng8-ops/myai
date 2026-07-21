from typing import Literal

from core.models.base import BaseConfig
from selector.config.enums import SelectorType



class SelectorConfig(BaseConfig):
    type: SelectorType
    selector: str

    many: bool = False
    extract: Literal["text", "html"] | None = "text"
    attribute: str | None = None