

from transform.config.enums import TransformType
from transform.config.base import TransformConfig


class ReplaceTransformConfig(TransformConfig):
    type: TransformType = TransformType.REPLACE
    pattern: str
    replacement: str