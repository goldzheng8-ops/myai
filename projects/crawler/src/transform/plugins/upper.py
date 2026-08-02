from models.config.transform.base import TransformConfig
from models.config.transform.upper import UpperTransformConfig
from transform.base import TransformPlugin


class UpperTransform(TransformPlugin[str, str]):
    type = UpperTransformConfig.type

    def transform_one(self, value: str, config: TransformConfig) -> str:
        if not isinstance(config, UpperTransformConfig):
            raise TypeError(f"UpperTransform expects UpperTransformConfig, got {type(config).__name__}")
        return value.upper()