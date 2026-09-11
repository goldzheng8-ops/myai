from __future__ import annotations
from collections.abc import Mapping
from typing import TextIO
import asyncio
import csv
from pathlib import Path
from typing import Any

from core.output.config import CsvOutputConfig
from core.output.model import OutputItem
from core.output.sink.base import OutputSink


class CsvOutputSink(
    OutputSink[CsvOutputConfig],
):

    def __init__(
        self,
        config: CsvOutputConfig,
    ) -> None:
        super().__init__(config)

        self._file: TextIO | None = None
        self._writer: csv.DictWriter[str] | None = None
        self._fieldnames: tuple[str, ...] | None = None
        self._header_written = False

    async def start(self) -> None:
        if self._file is not None:
            return

        path = Path(self.config.path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_exists = path.exists()
        file_has_content = (
            file_exists
            and path.stat().st_size > 0
        )

        if self.config.append and file_exists:
            mode = "a"
        else:
            mode = "w"

        file = open(
            path,
            mode=mode,
            encoding=self.config.encoding,
            newline="",
        )

        self._file = file

        if self.config.append and file_has_content:
            with path.open(
                mode="r",
                encoding=self.config.encoding,
                newline="",
            ) as existing_file:
                reader = csv.reader(existing_file)
                header = next(reader, None)

            if header:
                self._fieldnames = tuple(header)
                self._header_written = True
                self._writer = csv.DictWriter(
                    file,
                    fieldnames=self._fieldnames,
                )

    async def write(
        self,
        item: OutputItem,
    ) -> None:
        file = self._file

        if file is None:
            raise RuntimeError(
                "CsvOutputSink is not open.",
            )

        if not isinstance(item.data, Mapping):
            raise TypeError(
                "CsvOutputSink requires "
                "OutputItem.data to be a mapping.",
            )

        data: Mapping[Any, Any] = item.data

        row: dict[str, Any] = {
            str(key): value
            for key, value in data.items()
        }

        if self._fieldnames is None:
            self._fieldnames = tuple(row.keys())
            self._writer = csv.DictWriter(
                file,
                fieldnames=self._fieldnames,
            )

        writer = self._writer

        if writer is None:
            raise RuntimeError(
                "CSV writer is not initialized.",
            )

        if not self._header_written:
            await asyncio.to_thread(
                writer.writeheader,
            )
            self._header_written = True

        expected = set(self._fieldnames)
        actual = set(row)

        if actual != expected:
            raise ValueError(
                "CSV row fields do not match "
                "the initial schema.",
            )

        await asyncio.to_thread(
            writer.writerow,
            row,
        )

    async def close(self) -> None:
        file = self._file

        if file is None:
            return

        self._file = None

        await asyncio.to_thread(
            file.flush,
        )

        await asyncio.to_thread(
            file.close,
        )

        self._writer = None
        self._fieldnames = None
        self._header_written = False