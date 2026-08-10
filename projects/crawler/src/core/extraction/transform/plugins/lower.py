from models.config.transform.base import TransformConfig
from models.config.transform.lower import LowerTransformConfig
from core.extraction.transform.base import TransformPlugin


class LowerTransform(TransformPlugin[str, str, LowerTransformConfig]):
    type = LowerTransformConfig.type

    def transform_one(self, value: str, config: TransformConfig) -> str:
        if not isinstance(config, LowerTransformConfig):
            raise TypeError(f"LowerTransform expects LowerTransformConfig, got {type(config).__name__}")
        return value.lower()