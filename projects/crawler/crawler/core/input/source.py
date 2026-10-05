from enum import StrEnum

from core.typing.config import BaseConfig

class DataFormat(StrEnum):
    CSV = "csv"
    JSON = "json"
    EXCEL = "excel"



class DataSource(BaseConfig):
    format: DataFormat
    path: str