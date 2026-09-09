from core.extraction.transform.config import  UpperTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.typing import TransformType

class UpperTransform(TransformPlugin[str, str,UpperTransformConfig]):
    plugin_type = TransformType.UPPER

    def transform_one(self, value: str, config: UpperTransformConfig) -> str:
        return value.upper()