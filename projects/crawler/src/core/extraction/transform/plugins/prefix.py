from core.extraction.transform.config import  PrefixTransformConfig
from core.extraction.transform.base import TransformPlugin


class PrefixTransform(TransformPlugin[str, str, PrefixTransformConfig]):
    plugin_type = PrefixTransformConfig.type

    def transform_one(self, value: str, config: PrefixTransformConfig) -> str:

        return f"{config.prefix}{value}"
