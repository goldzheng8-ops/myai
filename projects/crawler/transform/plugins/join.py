from transform.config.enums import TransformType
from transform.base import TransformPlugin
from transform.config.join import JoinTransformConfig


class JoinTransform(TransformPlugin[JoinTransformConfig]):
    
    @property
    def type(self)->TransformType:
        return TransformType.DATETIME

    def transform_one(
        self,
        value: str,
        config:JoinTransformConfig ,
    ):
        ...