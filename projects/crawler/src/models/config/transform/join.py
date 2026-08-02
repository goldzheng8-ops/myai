from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig


class JoinTransformConfig(TransformConfig):
    type: TransformType = TransformType.JOIN
    separator: str = ""