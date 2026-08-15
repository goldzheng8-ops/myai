from enum import Enum
from typing import TypeVar

from core.extraction.transform.config import TransformConfig

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")
ConfigT=TypeVar("ConfigT", bound=TransformConfig)

class TransformType(str,Enum):

    STRIP="strip"

    LOWER="lower"

    UPPER="upper"

    TO_INT="to_int"

    TO_FLOAT="to_float"

    DATETIME="datetime"

    PREFIX="prefix"

    SUFFIX="suffix"

    REPLACE="replace"

    JOIN="join"

    NUMBER="number"

    REGEX="regex"

    SPLIT="split"