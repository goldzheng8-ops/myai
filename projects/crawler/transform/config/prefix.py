

from core.models.base import BaseConfig
from transform.config.base import TransformType


class PrefixTransformConfig(BaseConfig):
    type: TransformType = TransformType.PREFIX

    prefix: str