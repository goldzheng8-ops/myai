from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig

class SplitTransformConfig(TransformConfig):
    type: TransformType = TransformType.SPLIT
    separator: str = ""