import re

from models.config.transform.regex import RegexTransformConfig
from transform.base import TransformPlugin


class RegexTransform(TransformPlugin[str, str | None, RegexTransformConfig]):
    type = RegexTransformConfig.type

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