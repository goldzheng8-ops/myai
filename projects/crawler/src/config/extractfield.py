from typing import Any

from config.selector.base import SelectorConfig
from config.transform.base import TransformConfig
from pydantic import BaseModel, Field

class ExtractFieldConfig(BaseModel):

    name: str

    selector: SelectorConfig

    required: bool = False

    default: Any = None

    transforms: list[TransformConfig] = Field(default_factory=list)