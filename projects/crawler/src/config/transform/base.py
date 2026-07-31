from core.models.base import BaseConfig
from enums.transform_type import TransformType


class TransformConfig(BaseConfig):

    type: TransformType
