from transform.base import TransformPlugin
from transform.config.upper import UpperTransformConfig


class UpperTransform(TransformPlugin[str,str,UpperTransformConfig]):


    type=UpperTransformConfig.type

    def transform_one(self, value:str, config:UpperTransformConfig):
        # if not isinstance(value, str):
        #     raise TypeError(
        #         f"UpperTransform expects str, got {type(value).__name__}"
        #     )
        return value.upper()