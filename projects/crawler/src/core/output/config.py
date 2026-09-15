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

class JsonFileOutputConfig(OutputConfig):
    type: Literal["json_file"] = "json_file"

    path: str
    ensure_ascii: bool = False
    indent: int | None = None
    include_metadata: bool = False


class BinaryFileOutputConfig(OutputConfig):
    type: Literal["binary_file"] = "binary_file"

    directory: str
    filename: str | None = None
    overwrite: bool = False

OutputConfigUnion = Annotated[
    (
        JsonlOutputConfig
        | JsonFileOutputConfig
        | CsvOutputConfig
        | PostgresOutputConfig
        | BinaryFileOutputConfig
    ),
    Field(discriminator="type"),
]