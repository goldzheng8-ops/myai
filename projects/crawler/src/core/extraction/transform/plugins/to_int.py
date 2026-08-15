from core.extraction.transform.config import TransformConfig, ToIntTransformConfig
from core.extraction.transform.base import TransformPlugin


class ToIntTransform(TransformPlugin[str | int | float, int, ToIntTransformConfig]):
    type = ToIntTransformConfig.type

    def transform_one(self, value: str | int | float, config: TransformConfig) -> int:
        if not isinstance(config, ToIntTransformConfig):
            raise TypeError(f"ToIntTransform expects ToIntTransformConfig, got {type(config).__name__}")
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        return int(str(value).replace(",", "").replace("_", "").strip())
