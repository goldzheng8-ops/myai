from collections.abc import Iterable

from core.extraction.transform.config import TransformConfig,JoinTransformConfig
from core.extraction.transform.base import TransformPlugin


class JoinTransform(TransformPlugin[Iterable[str], str, JoinTransformConfig]):
    type = JoinTransformConfig.type

    def transform_one(
        self,
        value: Iterable[str],
        config: TransformConfig,
    ) -> str:
        if not isinstance(config, JoinTransformConfig):
            raise TypeError(f"JoinTransform expects JoinTransformConfig, got {type(config).__name__}")
        return config.separator.join(str(item) for item in value)