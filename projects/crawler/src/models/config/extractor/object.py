

from models.config.extractor.base import ExtractConfig
from models.enums.extract_type import ExtractType
from pydantic import Field

class ObjectConfig(ExtractConfig):

    type = ExtractType.OBJECT

    children: list[
        ExtractConfig
    ] = Field(default_factory=list)

