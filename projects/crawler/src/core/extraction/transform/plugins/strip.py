from core.extraction.transform.config import StripTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.context import TransformContext
from core.extraction.transform.typing import TransformType

class StripTransform(TransformPlugin[str, str, StripTransformConfig]):
    plugin_type = TransformType.STRIP

    def transform_one(self, value: str, config: StripTransformConfig, context: TransformContext | None = None) -> str:

        return value.strip(config.chars)