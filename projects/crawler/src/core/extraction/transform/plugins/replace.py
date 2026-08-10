from models.config.transform.base import TransformConfig
from models.config.transform.replace import ReplaceTransformConfig
from core.extraction.transform.base import TransformPlugin


class ReplaceTransform(TransformPlugin[str, str, ReplaceTransformConfig]):
    type = ReplaceTransformConfig.type

    def transform_one(
        self,
        value: str,
        config: TransformConfig,
    ) -> str:
        if not isinstance(config, ReplaceTransformConfig):
            raise TypeError(f"ReplaceTransform expects ReplaceTransformConfig, got {type(config).__name__}")
        return value.replace(
            config.pattern,
            config.replacement,
        )