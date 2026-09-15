
from enum import Enum
from typing import TypeVar


class OutputType(str, Enum):
    JSONL = "jsonl"
    JSON_FILE = "json_file"
    CSV = "csv"
    POSTGRES = "postgres"
    BINARY_FILE = "binary_file"

ConfigT = TypeVar(
    "ConfigT",
)