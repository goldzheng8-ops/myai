from core.extraction.transform.config import TransformConfig, UpperTransformConfig
from core.extraction.transform.base import TransformPlugin


class UpperTransform(TransformPlugin[str, str,TransformConfig]):
    type = UpperTransformConfig.type

    def transform_one(self, value: str, config: TransformConfig) -> str:
        if not isinstance(config, UpperTransformConfig):
            raise TypeError(f"UpperTransform expects UpperTransformConfig, got {type(config).__name__}")
        return value.upper()