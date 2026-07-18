from transform.config.datetime import DatetimeTransformConfig
from transform.config.enums import TransformType
from transform.base import TransformPlugin


class DateTimeTransform(TransformPlugin[DatetimeTransformConfig]):
    
    @property
    def type(self)->TransformType:
        return TransformType.DATETIME

    def transform_one(
        self,
        value: str,
        config: DatetimeTransformConfig,
    ):
        ...