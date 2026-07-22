

from transform.config.base import TransformConfig
from transform.config.enums import TransformType


class JoinTransformConfig(TransformConfig):
    type: TransformType = TransformType.JOIN
    separator: str = ""