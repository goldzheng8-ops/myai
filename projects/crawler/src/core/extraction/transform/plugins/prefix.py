from models.config.transform.base import TransformConfig
from models.config.transform.prefix import PrefixTransformConfig
from core.extraction.transform.base import TransformPlugin


class PrefixTransform(TransformPlugin[str, str, PrefixTransformConfig]):
    type = PrefixTransformConfig.type

    def transform_one(self, value: str, config: TransformConfig) -> str:
        if not isinstance(config, PrefixTransformConfig):
            raise TypeError(f"PrefixTransform expects PrefixTransformConfig, got {type(config).__name__}")
        return f"{config.prefix}{value}"
