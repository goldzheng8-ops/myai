from enum import Enum

class TemplateBackendType(str, Enum):

    JINJA = "jinja"

    LIQUID = "liquid"

    MAKO = "mako"





