

from datetime import datetime

from models.config.transform.base import TransformConfig
from models.config.transform.datetime import DatetimeTransformConfig
from core.extraction.transform.base import TransformPlugin


class DateTimeTransform(TransformPlugin[str, str, DatetimeTransformConfig]):
    type = DatetimeTransformConfig.type

    def transform_one(self, value: str, config: TransformConfig) -> str:
        if not isinstance(config, DatetimeTransformConfig):
            raise TypeError(f"DateTimeTransform expects DatetimeTransformConfig, got {type(config).__name__}")
        if isinstance(value, datetime):
            return value.strftime(config.format)
        return datetime.strptime(value, config.format).isoformat()