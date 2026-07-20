

    
from transform.base import TransformPlugin
from transform.config.datetime import DatetimeTransformConfig
from transform.config.upper import UpperTransformConfig


class DateTimeTransform(TransformPlugin[str,str,DatetimeTransformConfig]):



    type=UpperTransformConfig.type

    def transform_one(self, value:str, config:DatetimeTransformConfig):
        # if not isinstance(value, str):
        #     raise TypeError(
        #         f"UpperTransform expects str, got {type(value).__name__}"
        #     )
        return value.upper()