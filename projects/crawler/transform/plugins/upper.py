from transform.config.enums import TransformType
from transform.base import TransformPlugin
from transform.config.upper import UpperTransformConfig


class UpperTransform(TransformPlugin[UpperTransformConfig]):


    @property
    def type(self):
        return TransformType.UPPER

    def transform_one(self, value:str, config:UpperTransformConfig):
        return value.upper()