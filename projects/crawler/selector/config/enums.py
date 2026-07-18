from enum import Enum

class SelectorType(str, Enum):

    CSS = "css"

    XPATH = "xpath"

    JSONPATH = "jsonpath"

    REGEX = "regex"