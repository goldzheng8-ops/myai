from enum import Enum


class ResponseSource(str, Enum):
    HTTP = "http"
    SCRAPY = "scrapy"
    BROWSER = "browser"