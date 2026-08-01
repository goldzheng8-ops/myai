from typing import Any

from models.config.extractor.base import ExtractConfig
from models.config.transform.base import TransformConfig
from models.config.value.base import ValueConfig
from models.enums.extract_type import ExtractType
from pydantic import Field

class FieldConfig(ExtractConfig):

    type = ExtractType.FIELD

    source: ValueConfig

    required: bool = False

    default: Any = None

    transforms: list[
        TransformConfig
    ] = Field(default_factory=list)

