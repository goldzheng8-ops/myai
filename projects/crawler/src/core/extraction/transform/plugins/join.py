from collections.abc import Iterable

from core.extraction.transform.config import JoinTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.context import TransformContext
from core.extraction.transform.typing import TransformType

class JoinTransform(TransformPlugin[Iterable[str], str, JoinTransformConfig]):
    plugin_type = TransformType.JOIN

    def transform_one(
        self,
        value: Iterable[str],
        config: JoinTransformConfig,
        context: TransformContext | None = None,
    ) -> str:

        return config.separator.join(str(item) for item in value)