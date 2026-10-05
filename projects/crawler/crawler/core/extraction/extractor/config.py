from __future__ import annotations
from typing import Annotated, Any, Literal
from pydantic import Field

from core.typing.config import BaseConfig
from core.extraction.selector.config import SelectorConfigUnion
from core.extraction.value.config import ValueConfigUnion
from core.extraction.transform.config import TransformConfigUnion

from .typing import ExtractType

class ExtractConfig(BaseConfig):
    name: str
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class FieldConfig(ExtractConfig):
    type: Literal[ExtractType.FIELD] = ExtractType.FIELD

    source: ValueConfigUnion

    required: bool = False
    default: Any = None

    transforms: list[TransformConfigUnion] = Field(
        default_factory=list,
    )


class ListConfig(ExtractConfig):
    type: Literal[ExtractType.LIST] = ExtractType.LIST

    selector: SelectorConfigUnion
    item: ExtractConfigUnion


class ObjectConfig(ExtractConfig):
    type: Literal[ExtractType.OBJECT] = ExtractType.OBJECT

    children: list[ExtractConfigUnion] = Field(
        default_factory=list,
    )

ExtractConfigUnion = Annotated[
    (
        FieldConfig
        | ListConfig
        | ObjectConfig
    ),
    Field(discriminator="type"),
]