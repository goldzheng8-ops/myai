import re
from core.extraction.transform.config import RegexTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.typing import TransformType

class RegexTransform(TransformPlugin[str, str | None, RegexTransformConfig]):
    plugin_type = TransformType.DATETIME

    def transform_one(
        self,
        value: str,
        config: RegexTransformConfig,
    ) -> str | None:
        if config.replacement is None:
            match = re.search(config.pattern, value)
            return match.group(0) if match else None

        return re.sub(
            config.pattern,
            config.replacement,
            value,
        )