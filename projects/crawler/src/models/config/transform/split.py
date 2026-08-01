from transform.config.enums import TransformType
from transform.config.base import TransformConfig

class SplitTransformConfig(TransformConfig):
    type: TransformType = TransformType.SPLIT
    separator: str = ""