

from transform.config.enums import TransformType
from transform.config.base import TransformConfig


class NumberTransformConfig(TransformConfig):
    type: TransformType = TransformType.NUMBER