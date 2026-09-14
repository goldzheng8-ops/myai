from core.extraction.transform.config import ReplaceTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.context import TransformContext
from core.extraction.transform.typing import TransformType

class ReplaceTransform(TransformPlugin[str, str, ReplaceTransformConfig]):
    plugin_type = TransformType.REPLACE

    def transform_one(
        self,
        value: str,
        config: ReplaceTransformConfig,
        context: TransformContext | None = None,
    ) -> str:

        return value.replace(
            config.pattern,
            config.replacement,
        )