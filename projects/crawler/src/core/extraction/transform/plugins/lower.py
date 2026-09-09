from core.extraction.transform.config import LowerTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.typing import TransformType

class LowerTransform(TransformPlugin[str, str, LowerTransformConfig]):
    plugin_type = TransformType.LOWER

    def transform_one(self, value: str, config: LowerTransformConfig) -> str:
        return value.lower()