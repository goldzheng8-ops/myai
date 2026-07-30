from typing import Any

from config.extractor.base import ExtractConfig
from config.transform.base import TransformConfig
from config.value.base import ValueConfig
from enums.extract_type import ExtractType
from pydantic import Field

class FieldConfig(ExtractConfig):

    type = ExtractType.FIELD

    source: ValueConfig

    required: bool = False

    default: Any = None

    transforms: list[
        TransformConfig
    ] = Field(default_factory=list)

