from typing import Any
from pydantic import Field

from core.models.base import BaseConfig
from enums.extract_type import ExtractType

class ExtractConfig(BaseConfig):

    type: ExtractType

    name: str

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )