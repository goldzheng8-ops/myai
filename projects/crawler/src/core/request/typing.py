from enum import Enum
from typing import Any, TypeAlias


class HttpMethod(str, Enum):

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class RequestKind(str, Enum):

    LIST = "list"
    DETAIL = "detail"
    LOGIN = "login"
    DOWNLOAD = "download"
    API = "api"


class DownloaderType(str, Enum):

    SCRAPY = "scrapy"
    PLAYWRIGHT = "playwright"


class ResponseFormat(str, Enum):

    HTML = "html"
    JSON = "json"
    TEXT = "text"


RequestHeaders: TypeAlias = dict[str, str]

RequestCookies: TypeAlias = dict[str, str]

RequestParams: TypeAlias = dict[str, str]

RequestBody: TypeAlias = Any

RequestExtra: TypeAlias = dict[str, Any]

'''
RequestParamValue: TypeAlias = (
    str | int | float | bool
)

RequestParams: TypeAlias = dict[
    str,
    RequestParamValue,
]
'''