from typing import Annotated, Literal

from pydantic import Field
from core.typing.config import BaseConfig
from core.extraction.transform.typing import TransformType





class DatetimeTransformConfig(BaseConfig):
    type: Literal[TransformType.DATETIME] = TransformType.DATETIME
    format: str


class JoinTransformConfig(BaseConfig):
    type: Literal[TransformType.JOIN] = TransformType.JOIN
    separator: str = ""


class LowerTransformConfig(BaseConfig):
    type: Literal[TransformType.LOWER] = TransformType.LOWER


class NumberTransformConfig(BaseConfig):
    type: Literal[TransformType.NUMBER] = TransformType.NUMBER


class PrefixTransformConfig(BaseConfig):
    type: Literal[TransformType.PREFIX] = TransformType.PREFIX
    value: str


class RegexTransformConfig(BaseConfig):
    type: Literal[TransformType.REGEX] = TransformType.REGEX
    pattern: str
    replacement: str | None = None


class ReplaceTransformConfig(BaseConfig):
    type: Literal[TransformType.REPLACE] = TransformType.REPLACE
    pattern: str
    replacement: str


class SplitTransformConfig(BaseConfig):
    type: Literal[TransformType.SPLIT] = TransformType.SPLIT
    separator: str = ""


class StripTransformConfig(BaseConfig):
    type: Literal[TransformType.STRIP] = TransformType.STRIP
    chars: str | None = None


class SuffixTransformConfig(BaseConfig):
    type: Literal[TransformType.SUFFIX] = TransformType.SUFFIX
    suffix: str


class ToFloatConfig(BaseConfig):
    type: Literal[TransformType.TO_FLOAT] = TransformType.TO_FLOAT


class ToIntTransformConfig(BaseConfig):
    type: Literal[TransformType.TO_INT] = TransformType.TO_INT


class UpperTransformConfig(BaseConfig):
    type: Literal[TransformType.UPPER] = TransformType.UPPER

class UrlResolveTransformConfig(BaseConfig):
    type: Literal[TransformType.URL_RESOLVE] = (
        TransformType.URL_RESOLVE
    )

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
        | UrlResolveTransformConfig
    ),
    Field(discriminator="type"),
]