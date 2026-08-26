from core.extraction.transform.config import  UpperTransformConfig
from core.extraction.transform.base import TransformPlugin


class UpperTransform(TransformPlugin[str, str,UpperTransformConfig]):
    plugin_type = UpperTransformConfig.type

    def transform_one(self, value: str, config: UpperTransformConfig) -> str:
        return value.upper()