from transform.config.enums import TransformType
from transform.base import TransformPlugin
from transform.config.number import NumberTransformConfig



class NumberTransform(TransformPlugin[NumberTransformConfig]):


    @property
    def type(self):
        return TransformType.NUMBER

    def transform_one(self, value:str, config:NumberTransformConfig):
        ...