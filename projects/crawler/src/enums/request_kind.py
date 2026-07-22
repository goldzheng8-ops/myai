

from enum import Enum


class RequestKind(str,Enum):

    LIST = "list"

    DETAIL = "detail"

    LOGIN = "login"

    DOWNLOAD = "download"

    API = "api"