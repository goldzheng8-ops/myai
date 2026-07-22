from enum import Enum


class ResponseFormat(str,Enum):

    HTML = "html"

    JSON = "json"

    XML = "xml"

    RSS = "rss"

    TEXT = "text"

    BINARY = "binary"