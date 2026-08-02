from models.enums.transform_type import TransformType
from models.config.transform.base import TransformConfig

class ReplaceTransformConfig(TransformConfig):
    type: TransformType = TransformType.REPLACE
    pattern: str
    replacement: str