from transform.config.enums import TransformType
from transform.config.base import TransformConfig


class UpperTransformConfig(TransformConfig):
    type: TransformType = TransformType.UPPER