from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig

class ToIntTransformConfig(TransformConfig):
    type:TransformType =TransformType.TO_INT