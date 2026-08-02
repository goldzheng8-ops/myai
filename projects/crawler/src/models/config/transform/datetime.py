from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig

class DatetimeTransformConfig(TransformConfig):
    type: TransformType = TransformType.DATETIME
    format: str