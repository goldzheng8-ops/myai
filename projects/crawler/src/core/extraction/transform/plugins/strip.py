from core.extraction.transform.config import StripTransformConfig
from core.extraction.transform.base import TransformPlugin


class StripTransform(TransformPlugin[str, str, StripTransformConfig]):
    plugin_type = StripTransformConfig.type

    def transform_one(self, value: str, config: StripTransformConfig) -> str:

        return value.strip(config.chars)