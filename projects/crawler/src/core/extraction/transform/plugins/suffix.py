from core.extraction.transform.config import SuffixTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.typing import TransformType

class SuffixTransform(TransformPlugin[str, str, SuffixTransformConfig]):
    plugin_type = TransformType.DATETIME

    def transform_one(self, value: str, config: SuffixTransformConfig) -> str:

        return f"{value}{config.suffix}"
