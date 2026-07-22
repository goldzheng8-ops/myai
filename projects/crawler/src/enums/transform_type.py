from enum import Enum


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