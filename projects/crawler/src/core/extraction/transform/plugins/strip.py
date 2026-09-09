from core.extraction.transform.config import StripTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.typing import TransformType

class StripTransform(TransformPlugin[str, str, StripTransformConfig]):
    plugin_type = TransformType.STRIP

    def transform_one(self, value: str, config: StripTransformConfig) -> str:

        return value.strip(config.chars)