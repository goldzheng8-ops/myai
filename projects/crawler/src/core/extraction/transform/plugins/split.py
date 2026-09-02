from core.extraction.transform.config import SplitTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.typing import TransformType

class SplitTransform(TransformPlugin[str, list[str], SplitTransformConfig]):
    plugin_type = TransformType.DATETIME

    def transform_one(
        self,
        value: str,
        config: SplitTransformConfig,
    ) -> list[str]:

        if config.separator:
            return value.split(config.separator)
        return value.split()