from core.extraction.transform.config import  PrefixTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.typing import TransformType

class PrefixTransform(TransformPlugin[str, str, PrefixTransformConfig]):
    plugin_type = TransformType.DATETIME

    def transform_one(self, value: str, config: PrefixTransformConfig) -> str:

        return f"{config.prefix}{value}"
