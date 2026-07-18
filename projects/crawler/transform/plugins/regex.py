import re

from transform.base import TransformPlugin
from transform.config.regex import RegexTransformConfig
from transform.config.enums import TransformType


class RegexTransformPlugin(TransformPlugin[RegexTransformConfig]):

    @property
    def type(self):
        return TransformType.REGEX

    def transform_one(
        self,
        value: str,
        config: RegexTransformConfig,
    ):

        if config.replacement is None:
            match = re.search(config.pattern, value)

            return match.group(0) if match else None

        return re.sub(
            config.pattern,
            config.replacement,
            value,
        )