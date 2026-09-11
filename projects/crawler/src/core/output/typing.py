
from enum import Enum
from typing import TypeVar


class OutputType(str,Enum):
    JSONL = "jsonl"
    CSV = "csv"
    POSTGRES ="postgres"

ConfigT = TypeVar(
    "ConfigT",
)