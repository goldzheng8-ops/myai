from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig

class StripTransformConfig(TransformConfig):
    type: TransformType = TransformType.STRIP
    chars: str | None = None
