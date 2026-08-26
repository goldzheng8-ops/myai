from core.extraction.transform.config import ToFloatConfig
from core.extraction.transform.base import TransformPlugin


class ToFloatTransform(TransformPlugin[str | int | float, float, ToFloatConfig]):
    plugin_type = ToFloatConfig.type

    def transform_one(self, value: str | int | float, config: ToFloatConfig) -> float:

        if isinstance(value, bool):
            return float(value)
        if isinstance(value, (int, float)):
            return float(value)
        return float(str(value).replace(",", "").replace("_", "").strip())
