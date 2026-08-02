from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig

class NumberTransformConfig(TransformConfig):
    type: TransformType = TransformType.NUMBER