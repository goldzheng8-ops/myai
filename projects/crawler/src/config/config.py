from __future__ import annotations

from enum import Enum
class BrowserEngine(str, Enum):

    PLAYWRIGHT = "playwright"

    SELENIUM = "selenium"

    SCRAPY = "scrapy"

class OutputFormat(str, Enum):

    JSON = "json"

    CSV = "csv"

    XLSX = "xlsx"

    DATABASE = "database"

    HTTP = "http"

class BrowserWaitUntil(str,Enum):
    
    LOAD="load"

    DOMCONTENTLOADED="domcontentloaded"

    NETWORKIDLE="networkidle"

