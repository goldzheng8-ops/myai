

from core.models.base import BaseConfig
from transform.config.enums import TransformType


class ToIntTransformConfig(BaseConfig):
    type:TransformType =TransformType.TO_INT