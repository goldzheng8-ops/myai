from collections.abc import Iterable

from core.extraction.transform.config import JoinTransformConfig
from core.extraction.transform.base import TransformPlugin


class JoinTransform(TransformPlugin[Iterable[str], str, JoinTransformConfig]):
    plugin_type = JoinTransformConfig.type

    def transform_one(
        self,
        value: Iterable[str],
        config: JoinTransformConfig,
    ) -> str:

        return config.separator.join(str(item) for item in value)