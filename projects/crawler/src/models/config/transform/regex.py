from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig


class RegexTransformConfig(TransformConfig):
    type: TransformType = TransformType.REGEX
    pattern: str
    replacement: str | None = None