from core.models.base import BaseConfig
from transform.config.enums import TransformType

class TransformConfig(BaseConfig):

    type: TransformType
