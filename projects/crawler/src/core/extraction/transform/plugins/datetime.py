

from datetime import datetime

from core.extraction.transform.config import DatetimeTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.context import TransformContext
from core.extraction.transform.typing import TransformType


class DateTimeTransform(TransformPlugin[str, str, DatetimeTransformConfig]):
    plugin_type = TransformType.DATETIME

    def transform_one(self, value: str|datetime, config: DatetimeTransformConfig,context: TransformContext | None = None,) -> str:
        if isinstance(value, datetime):
            return value.strftime(config.format)
        return datetime.strptime(value, config.format).isoformat()