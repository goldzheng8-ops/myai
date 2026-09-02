from core.extraction.transform.config import NumberTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.typing import TransformType

class NumberTransform(TransformPlugin[str | int | float, int | float, NumberTransformConfig]):
    plugin_type = TransformType.DATETIME

    def transform_one(
        self,
        value: str | int | float,
        config: NumberTransformConfig,
    ) -> int | float:
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, (int, float)):
            return value

        normalized = value.strip().replace(",", "").replace("_", "")
        if not normalized:
            raise ValueError("number transform received an empty value")

        if "." in normalized or "e" in normalized.lower():
            return float(normalized)
        return int(normalized)