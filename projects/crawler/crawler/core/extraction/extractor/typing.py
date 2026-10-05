from enum import Enum


class ExtractType(str,Enum):
    FIELD = "field"
    OBJECT = "object"
    LIST = "list"