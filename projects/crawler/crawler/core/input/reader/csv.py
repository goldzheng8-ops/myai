import csv
from collections.abc import Iterable
from pathlib import Path

from core.input.reader.base import BaseDataReader
from core.input.record import DataRecord
from core.input.source import DataFormat, DataSource


class CsvDataReader(
    BaseDataReader,
):
    format = DataFormat.CSV

    def _read(
        self,
        source: DataSource,
    ) -> Iterable[DataRecord]:
        path = Path(source.path)

        with path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError(
                    f"CSV file {path} does not contain "
                    "a header row.",
                )

            for row in reader:
                yield DataRecord(
                    values=dict(row),
                )