from enum import Enum

class ExtensionKind(str, Enum):

    FILTER = "filter"

    TEST = "test"

    GLOBAL = "global"