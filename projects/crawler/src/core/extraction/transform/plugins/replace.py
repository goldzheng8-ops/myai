from core.extraction.transform.config import ReplaceTransformConfig
from core.extraction.transform.base import TransformPlugin


class ReplaceTransform(TransformPlugin[str, str, ReplaceTransformConfig]):
    plugin_type = ReplaceTransformConfig.type

    def transform_one(
        self,
        value: str,
        config: ReplaceTransformConfig,
    ) -> str:

        return value.replace(
            config.pattern,
            config.replacement,
        )