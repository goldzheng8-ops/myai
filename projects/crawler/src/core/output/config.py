from typing import Annotated, Literal

from core.typing.config import BaseConfig
from pydantic import Field
class OutputConfig(BaseConfig):
    name: str


class JsonlOutputConfig(OutputConfig):
    type: Literal["jsonl"] = "jsonl"

    path: str
    ensure_ascii: bool = False
    include_metadata: bool = False

class CsvOutputConfig(OutputConfig):
    type: Literal["csv"] = "csv"

    path: str
    encoding: str = "utf-8"
    append: bool = False

class PostgresOutputConfig(OutputConfig):
    type: Literal["postgres"] = "postgres"

    table: str
    dsn: str


OutputConfigUnion = Annotated[
    (
        JsonlOutputConfig
        | CsvOutputConfig
        | PostgresOutputConfig
    ),
    Field(discriminator="type"),
]