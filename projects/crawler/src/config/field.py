from typing import Any

from config.transform.base import TransformConfig
from config.value.base import ValueConfig
from pydantic import BaseModel, Field

class FieldConfig(BaseModel):

    name: str

    source: ValueConfig

    required: bool = False

    default: Any = None

    transforms: list[TransformConfig] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)