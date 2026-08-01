from models.config.base import BaseConfig
from models.enums.transform_type import TransformType


class TransformConfig(BaseConfig):

    type: TransformType
