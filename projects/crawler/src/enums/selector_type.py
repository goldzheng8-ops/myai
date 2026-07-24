from enum import Enum

class SelectorType(str, Enum):

    CSS = "css"

    XPATH = "xpath"

    REGEX = "regex"

    JMESPATH = "jmespath"

    JSONPATH = "jsonpath"