from core.extraction.transform.config import SuffixTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.context import TransformContext
from core.extraction.transform.typing import TransformType

class SuffixTransform(TransformPlugin[str, str, SuffixTransformConfig]):
    plugin_type = TransformType.SUFFIX

    def transform_one(self, value: str, config: SuffixTransformConfig, context: TransformContext | None = None) -> str:

        return f"{value}{config.suffix}"
