from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig


class LowerTransformConfig(TransformConfig):
    type: TransformType = TransformType.LOWER