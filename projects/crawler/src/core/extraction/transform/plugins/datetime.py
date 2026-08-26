

from datetime import datetime

from core.extraction.transform.config import DatetimeTransformConfig
from core.extraction.transform.base import TransformPlugin


class DateTimeTransform(TransformPlugin[str, str, DatetimeTransformConfig]):
    plugin_type = DatetimeTransformConfig.type

    def transform_one(self, value: str|datetime, config: DatetimeTransformConfig) -> str:
        if isinstance(value, datetime):
            return value.strftime(config.format)
        return datetime.strptime(value, config.format).isoformat()