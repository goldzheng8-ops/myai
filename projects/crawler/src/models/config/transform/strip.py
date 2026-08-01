from transform.config.enums import TransformType
from transform.config.base import TransformConfig

class StripTransformConfig(TransformConfig):
    type: TransformType = TransformType.STRIP
    chars: str | None = None
