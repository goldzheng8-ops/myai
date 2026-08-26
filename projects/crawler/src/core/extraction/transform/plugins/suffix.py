from core.extraction.transform.config import SuffixTransformConfig
from core.extraction.transform.base import TransformPlugin


class SuffixTransform(TransformPlugin[str, str, SuffixTransformConfig]):
    plugin_type = SuffixTransformConfig.type

    def transform_one(self, value: str, config: SuffixTransformConfig) -> str:

        return f"{value}{config.suffix}"
