from models.config.transform.base import TransformConfig
from models.config.transform.strip import StripTransformConfig
from transform.base import TransformPlugin


class StripTransform(TransformPlugin[str, str, StripTransformConfig]):
    type = StripTransformConfig.type

    def transform_one(self, value: str, config: TransformConfig) -> str:
        if not isinstance(config, StripTransformConfig):
            raise TypeError(f"StripTransform expects StripTransformConfig, got {type(config).__name__}")
        return value.strip(config.chars)