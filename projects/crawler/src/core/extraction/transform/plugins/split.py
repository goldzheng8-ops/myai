from core.extraction.transform.config import TransformConfig, SplitTransformConfig
from core.extraction.transform.base import TransformPlugin


class SplitTransform(TransformPlugin[str, list[str], SplitTransformConfig]):
    type = SplitTransformConfig.type

    def transform_one(
        self,
        value: str,
        config: TransformConfig,
    ) -> list[str]:
        if not isinstance(config, SplitTransformConfig):
            raise TypeError(f"SplitTransform expects SplitTransformConfig, got {type(config).__name__}")
        if config.separator:
            return value.split(config.separator)
        return value.split()