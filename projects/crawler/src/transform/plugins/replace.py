
from transform.config.enums import TransformType
from transform.base import TransformPlugin
from transform.config.replace import ReplaceTransformConfig


class ReplaceTransformPlugin(TransformPlugin[ReplaceTransformConfig]):

    @property
    def type(self)->TransformType:
        return TransformType.REPLACE

    def transform_one(
        self,
        value: str,
        config: ReplaceTransformConfig,
    ):
        return value.replace(
            config.pattern,
            config.replacement,
        )