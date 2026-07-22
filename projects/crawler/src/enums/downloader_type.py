from enum import Enum

class DownloaderType(str, Enum):

    PLAYWRIGHT="playwright"
    AIOHTTP="aiohttp"
    HTTPX="httpx"
    REQUESTS="requests"