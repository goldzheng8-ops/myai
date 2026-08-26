from core.extraction.transform.config import SplitTransformConfig
from core.extraction.transform.base import TransformPlugin


class SplitTransform(TransformPlugin[str, list[str], SplitTransformConfig]):
    plugin_type = SplitTransformConfig.type

    def transform_one(
        self,
        value: str,
        config: SplitTransformConfig,
    ) -> list[str]:

        if config.separator:
            return value.split(config.separator)
        return value.split()