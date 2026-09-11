from __future__ import annotations

import csv

import pytest

from core.output.config import CsvOutputConfig
from core.output.model import OutputItem
from core.output.sink.csv import CsvOutputSink


@pytest.mark.asyncio
async def test_csv_sink_writes_header_and_rows(tmp_path):
    csv_path = tmp_path / "output.csv"
    sink = CsvOutputSink(
        CsvOutputConfig(
            name="items",
            path=str(csv_path),
            encoding="utf-8",
            append=False,
        )
    )

    await sink.open()
    await sink.write(
        OutputItem(
            data={"name": "alice", "age": 42},
            spider="demo",
        )
    )
    await sink.write(
        OutputItem(
            data={"name": "bob", "age": 24},
            spider="demo",
        )
    )
    await sink.close()

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    assert rows == [
        {"name": "alice", "age": "42"},
        {"name": "bob", "age": "24"},
    ]


@pytest.mark.asyncio
async def test_csv_sink_appends_without_repeating_header(tmp_path):
    csv_path = tmp_path / "output.csv"
    csv_path.write_text("name,age\nalice,42\n", encoding="utf-8")

    sink = CsvOutputSink(
        CsvOutputConfig(
            name="items",
            path=str(csv_path),
            encoding="utf-8",
            append=True,
        )
    )

    await sink.open()
    await sink.write(
        OutputItem(
            data={"name": "bob", "age": 24},
            spider="demo",
        )
    )
    await sink.close()

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    assert rows == [
        {"name": "alice", "age": "42"},
        {"name": "bob", "age": "24"},
    ]
