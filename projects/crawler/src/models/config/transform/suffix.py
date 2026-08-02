from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig

class SuffixTransformConfig(TransformConfig):
    type: TransformType = TransformType.SUFFIX

    suffix: str