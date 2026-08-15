from core.extraction.transform.config import TransformConfig, StripTransformConfig
from core.extraction.transform.base import TransformPlugin


class StripTransform(TransformPlugin[str, str, StripTransformConfig]):
    type = StripTransformConfig.type

    def transform_one(self, value: str, config: TransformConfig) -> str:
        if not isinstance(config, StripTransformConfig):
            raise TypeError(f"StripTransform expects StripTransformConfig, got {type(config).__name__}")
        return value.strip(config.chars)