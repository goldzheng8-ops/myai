from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import aiofiles

from core.output.config import JsonlOutputConfig
from core.output.model import OutputItem
from core.output.sink.base import OutputSink


class JsonlOutputSink(
    OutputSink[JsonlOutputConfig],
):

    def __init__(
        self,
        config: JsonlOutputConfig,
    ) -> None:
        super().__init__(config)
        self._file = None

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
            mode="a",
            encoding="utf-8",
        )

    async def write(
        self,
        item: OutputItem,
    ) -> None:
        if self._file is None:
            raise RuntimeError(
                "JsonlOutputSink is not open.",
            )
        if self.config.include_metadata is True:
            record: dict[str, Any] = {
                "data": item.data,
                "spider": item.spider,
                "metadata": dict(item.metadata),
            }
        else:
            record=item.data

        line = json.dumps(
            record,
            ensure_ascii=self.config.ensure_ascii,
            default=str,
        )

        await self._file.write(
            line + "\n",
        )

    async def close(self) -> None:
        if self._file is None:
            return

        file = self._file
        self._file = None

        await file.flush()
        await file.close()