from typing import Annotated, Literal

from pydantic import Field
from core.typing.config import BaseConfig
from core.extraction.transform.typing import TransformType



class TransformConfig(BaseConfig):
    type: TransformType


class DatetimeTransformConfig(TransformConfig):
    type: Literal[TransformType.DATETIME] = TransformType.DATETIME
    format: str


class JoinTransformConfig(TransformConfig):
    type: Literal[TransformType.JOIN] = TransformType.JOIN
    separator: str = ""


class LowerTransformConfig(TransformConfig):
    type: Literal[TransformType.LOWER] = TransformType.LOWER


class NumberTransformConfig(TransformConfig):
    type: Literal[TransformType.NUMBER] = TransformType.NUMBER


class PrefixTransformConfig(TransformConfig):
    type: Literal[TransformType.PREFIX] = TransformType.PREFIX
    prefix: str


class RegexTransformConfig(TransformConfig):
    type: Literal[TransformType.REGEX] = TransformType.REGEX
    pattern: str
    replacement: str | None = None


class ReplaceTransformConfig(TransformConfig):
    type: Literal[TransformType.REPLACE] = TransformType.REPLACE
    pattern: str
    replacement: str


class SplitTransformConfig(TransformConfig):
    type: Literal[TransformType.SPLIT] = TransformType.SPLIT
    separator: str = ""


class StripTransformConfig(TransformConfig):
    type: Literal[TransformType.STRIP] = TransformType.STRIP
    chars: str | None = None


class SuffixTransformConfig(TransformConfig):
    type: Literal[TransformType.SUFFIX] = TransformType.SUFFIX
    suffix: str


class ToFloatConfig(TransformConfig):
    type: Literal[TransformType.TO_FLOAT] = TransformType.TO_FLOAT


class ToIntTransformConfig(TransformConfig):
    type: Literal[TransformType.TO_INT] = TransformType.TO_INT


class UpperTransformConfig(TransformConfig):
    type: Literal[TransformType.UPPER] = TransformType.UPPER

TransformConfigUnion = Annotated[
    (
        DatetimeTransformConfig
        | JoinTransformConfig
        | LowerTransformConfig
        | NumberTransformConfig
        | PrefixTransformConfig
        | RegexTransformConfig
        | ReplaceTransformConfig
        | SplitTransformConfig
        | StripTransformConfig
        | SuffixTransformConfig
        | ToFloatConfig
        | ToIntTransformConfig
        | UpperTransformConfig
    ),
    Field(discriminator="type"),
]