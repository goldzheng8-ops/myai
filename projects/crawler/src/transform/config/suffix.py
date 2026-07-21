

from core.models.base import BaseConfig
from transform.config.enums import TransformType


class SuffixTransformConfig(BaseConfig):
    type: TransformType = TransformType.SUFFIX

    suffix: str