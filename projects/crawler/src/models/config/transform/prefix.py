from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig

class PrefixTransformConfig(TransformConfig):
    type: TransformType = TransformType.PREFIX

    prefix: str