
from transform.config.enums import TransformType
from transform.base import TransformPlugin
from transform.config.strip import StripTransformConfig


class StripTransformPlugin(TransformPlugin[StripTransformConfig]):

    @property
    def type(self):
        return TransformType.STRIP

    def transform_one(self, value:str, config:StripTransformConfig):
        return value.strip()