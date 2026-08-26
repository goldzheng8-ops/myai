from core.extraction.transform.config import LowerTransformConfig
from core.extraction.transform.base import TransformPlugin


class LowerTransform(TransformPlugin[str, str, LowerTransformConfig]):
    plugin_type = LowerTransformConfig.type

    def transform_one(self, value: str, config: LowerTransformConfig) -> str:
        return value.lower()