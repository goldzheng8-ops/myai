
import json
from pathlib import Path
from typing import Any

import aiofiles
from core.output.config import JsonFileOutputConfig
from core.output.model import OutputItem
from core.output.sink.base import OutputSink


class JsonFileOutputSink(
    OutputSink[JsonFileOutputConfig],
):

    def __init__(
        self,
        config: JsonFileOutputConfig,
    ) -> None:
        super().__init__(config)
        self._file = None
        self._first = True

    async def start(self) -> None:
        if self._file is not None:
            return

        path = Path(self.config.path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._file = await aiofiles.open(
            path,
            mode="w",
            encoding="utf-8",
        )

        await self._file.write("[\n")

    async def write(
        self,
        item: OutputItem,
    ) -> None:
        if self._file is None:
            raise RuntimeError(
                "JsonFileOutputSink is not open.",
            )

        record: Any

        if self.config.include_metadata:
            record = {
                "data": item.data,
                "spider": item.spider,
                "metadata": dict(item.metadata),
            }
        else:
            record = item.data

        if not self._first:
            await self._file.write(",\n")

        text = json.dumps(
            record,
            ensure_ascii=self.config.ensure_ascii,
            indent=self.config.indent,
            default=str,
        )

        await self._file.write(text)

        self._first = False

    async def close(self) -> None:
        if self._file is None:
            return

        file = self._file
        self._file = None

        await file.write("\n]\n")
        await file.flush()
        await file.close()