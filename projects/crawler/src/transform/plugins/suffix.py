from models.config.transform.base import TransformConfig
from models.config.transform.suffix import SuffixTransformConfig
from transform.base import TransformPlugin


class SuffixTransform(TransformPlugin[str, str, SuffixTransformConfig]):
    type = SuffixTransformConfig.type

    def transform_one(self, value: str, config: TransformConfig) -> str:
        if not isinstance(config, SuffixTransformConfig):
            raise TypeError(f"SuffixTransform expects SuffixTransformConfig, got {type(config).__name__}")
        return f"{value}{config.suffix}"
