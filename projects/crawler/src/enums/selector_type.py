from enum import Enum

class SelectorType(str, Enum):

    CSS = "css"

    XPATH = "xpath"

    JMESPATH = "jmespath"

    REGEX = "regex"