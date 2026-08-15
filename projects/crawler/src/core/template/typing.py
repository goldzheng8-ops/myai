from enum import Enum

class TemplateBackendType(str, Enum):

    JINJA = "jinja"

    LIQUID = "liquid"

    MAKO = "mako"

class ExtensionKind(str, Enum):

    FILTER = "filter"

    TEST = "test"

    GLOBAL = "global"