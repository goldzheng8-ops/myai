

from transform.config.enums import TransformType
from transform.config.base import TransformConfig


class LowerTransformConfig(TransformConfig):
    type: TransformType = TransformType.LOWER