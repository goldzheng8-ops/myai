from models.config.transform.base import TransformConfig
from models.config.transform.to_float import ToFloatConfig
from core.extraction.transform.base import TransformPlugin


class ToFloatTransform(TransformPlugin[str | int | float, float, ToFloatConfig]):
    type = ToFloatConfig.type

    def transform_one(self, value: str | int | float, config: TransformConfig) -> float:
        if not isinstance(config, ToFloatConfig):
            raise TypeError(f"ToFloatTransform expects ToFloatConfig, got {type(config).__name__}")
        if isinstance(value, bool):
            return float(value)
        if isinstance(value, (int, float)):
            return float(value)
        return float(str(value).replace(",", "").replace("_", "").strip())
