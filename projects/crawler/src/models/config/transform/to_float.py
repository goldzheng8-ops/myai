from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig


class ToFloatConfig(TransformConfig):
    type: TransformType = TransformType.TO_FLOAT