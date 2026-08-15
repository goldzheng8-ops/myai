from typing import Any
from pydantic import Field

from core.typing.config import BaseConfig
from core.extraction.selector.config import SelectorConfig
from core.extraction.value.config import ValueConfig
from core.extraction.transform.config import TransformConfig

from .typing import ExtractType

class ExtractConfig(BaseConfig):

    type: ExtractType

    name: str

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

class FieldConfig(ExtractConfig):

    type = ExtractType.FIELD

    source: ValueConfig

    required: bool = False

    default: Any = None

    transforms: list[
        TransformConfig
    ] = Field(default_factory=list)

class ListConfig(ExtractConfig):

    type = ExtractType.LIST

    selector: SelectorConfig

    item: ExtractConfig

class ObjectConfig(ExtractConfig):

    type = ExtractType.OBJECT

    children: list[
        ExtractConfig
    ] = Field(default_factory=list)
