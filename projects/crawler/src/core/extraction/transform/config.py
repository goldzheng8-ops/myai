from core.typing.config import BaseConfig
from core.extraction.transform.typing import TransformType

class TransformConfig(BaseConfig):
    type: TransformType

class DatetimeTransformConfig(TransformConfig):
    type: TransformType = TransformType.DATETIME
    format: str

class JoinTransformConfig(TransformConfig):
    type: TransformType = TransformType.JOIN
    separator: str = ""

class LowerTransformConfig(TransformConfig):
    type: TransformType = TransformType.LOWER

class NumberTransformConfig(TransformConfig):
    type: TransformType = TransformType.NUMBER

class PrefixTransformConfig(TransformConfig):
    type: TransformType = TransformType.PREFIX
    prefix: str

class RegexTransformConfig(TransformConfig):
    type: TransformType = TransformType.REGEX
    pattern: str
    replacement: str | None = None

class ReplaceTransformConfig(TransformConfig):
    type: TransformType = TransformType.REPLACE
    pattern: str
    replacement: str

class SplitTransformConfig(TransformConfig):
    type: TransformType = TransformType.SPLIT
    separator: str = ""

class StripTransformConfig(TransformConfig):
    type: TransformType = TransformType.STRIP
    chars: str | None = None

class SuffixTransformConfig(TransformConfig):
    type: TransformType = TransformType.SUFFIX
    suffix: str

class ToFloatConfig(TransformConfig):
    type: TransformType = TransformType.TO_FLOAT

class ToIntTransformConfig(TransformConfig):
    type:TransformType =TransformType.TO_INT

class UpperTransformConfig(TransformConfig):
    type: TransformType = TransformType.UPPER