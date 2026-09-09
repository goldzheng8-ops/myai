from core.extraction.transform.config import ToFloatConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.typing import TransformType

class ToFloatTransform(TransformPlugin[str | int | float, float, ToFloatConfig]):
    plugin_type = TransformType.TO_FLOAT

    def transform_one(self, value: str | int | float, config: ToFloatConfig) -> float:

        if isinstance(value, bool):
            return float(value)
        if isinstance(value, (int, float)):
            return float(value)
        return float(str(value).replace(",", "").replace("_", "").strip())
