
from transform.config.enums import TransformType
from transform.config.base import TransformConfig


class DatetimeTransformConfig(TransformConfig):
    type: TransformType = TransformType.DATETIME
    format: str