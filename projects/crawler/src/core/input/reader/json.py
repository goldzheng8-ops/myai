import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from core.input.reader.base import BaseDataReader
from core.input.record import DataRecord
from core.input.source import DataFormat, DataSource


class JsonDataReader(
    BaseDataReader,
):
    format = DataFormat.JSON

    def _read(
        self,
        source: DataSource,
    ) -> Iterable[DataRecord]:
        path = Path(source.path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data: Any = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                f"JSON data source {path} must contain "
                "a top-level array.",
            )

        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(
                    f"JSON record at index {index} "
                    "must be an object.",
                )

            yield DataRecord(
                values=item,
            )