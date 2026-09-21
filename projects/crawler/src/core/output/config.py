from typing import Annotated, Literal

from core.output.typing import StorageType
from core.typing.config import BaseConfig
from pydantic import Field

class StorageConfig(BaseConfig):
    pass


class LocalStorageConfig(StorageConfig):
    type: Literal[StorageType.LOCAL] = StorageType.LOCAL

    directory: str


class S3StorageConfig(StorageConfig):

    type: Literal[StorageType.S3] = StorageType.S3

    bucket: str

    region: str = "us-east-1"

    endpoint_url: str | None = None

    access_key: str | None = None

    secret_key: str | None = None

    prefix: str = ""
    multipart_part_size: int = 8 * 1024 * 1024
    multipart_concurrency: int = 1

StorageConfigUnion = Annotated[
    LocalStorageConfig | S3StorageConfig,
    Field(
        discriminator="type",
    ),
]


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


class BinaryFileOutputConfig(
    OutputConfig,
):
    type: Literal["binary_file"] = "binary_file"

    storage: StorageConfigUnion

    filename: str = (
        "{{ download.filename or download.url | basename }}"
    )

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