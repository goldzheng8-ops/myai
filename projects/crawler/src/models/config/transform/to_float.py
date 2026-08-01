

from models.config.base import BaseConfig
from transform.config.enums import TransformType


class ToFloatConfig(BaseConfig):
    type: TransformType = TransformType.TO_FLOAT