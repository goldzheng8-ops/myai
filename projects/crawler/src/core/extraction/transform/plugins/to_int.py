from core.extraction.transform.config import ToIntTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.typing import TransformType

class ToIntTransform(TransformPlugin[str | int | float, int, ToIntTransformConfig]):
    plugin_type = TransformType.TO_INT

    def transform_one(self, value: str | int | float, config: ToIntTransformConfig) -> int:

        if isinstance(value, bool):
            return int(value)
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        return int(str(value).replace(",", "").replace("_", "").strip())
