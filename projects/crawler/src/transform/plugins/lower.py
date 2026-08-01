from transform.config.enums import TransformType
from transform.base import TransformPlugin
from transform.config.lower import LowerTransformConfig



class LowerTransform(TransformPlugin[LowerTransformConfig]):


    @property
    def type(self):
        return TransformType.UPPER

    def transform_one(self, value:str, config:LowerTransformConfig):
        return value.lower()