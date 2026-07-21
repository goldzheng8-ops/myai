


from transform.config.enums import TransformType
from transform.config.base import TransformConfig


class RegexTransformConfig(TransformConfig):
    type: TransformType = TransformType.REGEX
    pattern: str
    replacement: str | None = None