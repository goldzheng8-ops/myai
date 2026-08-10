from enum import Enum


class ExtractMode(str, Enum):

    TEXT = "text"

    HTML = "html"

    ATTRIBUTE="attribute"