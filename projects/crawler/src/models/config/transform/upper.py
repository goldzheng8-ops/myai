from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig


class UpperTransformConfig(TransformConfig):
    type: TransformType = TransformType.UPPER