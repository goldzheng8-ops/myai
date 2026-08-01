from transform.config.enums import TransformType
from transform.base import TransformPlugin
from transform.config.strip import StripTransformConfig


class StripTransform(TransformPlugin[StripTransformConfig]):
    
    @property
    def type(self)->TransformType:
        return TransformType.DATETIME

    def transform_one(
        self,
        value: str,
        config:StripTransformConfig ,
    ):
        ...