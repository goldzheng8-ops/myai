from __future__ import annotations

from collections.abc import Mapping
import re
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)

from core.output.config import PostgresOutputConfig
from core.output.model import OutputItem
from core.output.sink.base import OutputSink


_IDENTIFIER_PATTERN = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*$",
)


class PostgresOutputSink(
    OutputSink[PostgresOutputConfig],
):

    def __init__(
        self,
        config: PostgresOutputConfig,
    ) -> None:
        super().__init__(config)

        self._engine: AsyncEngine | None = None
        self._columns: tuple[str, ...] | None = None

    async def start(self) -> None:
        if self._engine is not None:
            return

        self._validate_identifier(
            self.config.table,
        )

        self._engine = create_async_engine(
            self.config.dsn,
        )

        async with self._engine.connect() as connection:
            await connection.execute(
                text("SELECT 1"),
            )

    async def write(
        self,
        item: OutputItem,
    ) -> None:

        if self._engine is None:
            raise RuntimeError(
                "PostgresOutputSink is not open.",
            )

        if not isinstance(item.data, Mapping):
            raise TypeError(
                "PostgresOutputSink requires "
                "OutputItem.data to be a mapping.",
            )

        data: Mapping[Any, Any] = item.data
        row = {
            str(key): value
            for key, value in data.items()
        }

        if not row:
            return

        columns = tuple(row.keys())

        if self._columns is None:
            self._columns = columns

        if columns != self._columns:
            raise ValueError(
                "PostgreSQL row fields do not match "
                "the initial schema.",
            )

        column_sql = ", ".join(
            self._quote_identifier(column)
            for column in columns
        )

        parameter_sql = ", ".join(
            f":{column}"
            for column in columns
        )

        statement = text(
            f"""
            INSERT INTO {self._quote_identifier(self.config.table)}
            ({column_sql})
            VALUES ({parameter_sql})
            """
        )

        async with self._engine.begin() as connection:
            await connection.execute(
                statement,
                row,
            )

    async def close(self) -> None:
        if self._engine is None:
            return

        engine = self._engine
        self._engine = None

        await engine.dispose()

        self._columns = None

    @staticmethod
    def _validate_identifier(
        value: str,
    ) -> None:
        if not _IDENTIFIER_PATTERN.fullmatch(value):
            raise ValueError(
                f"Invalid SQL identifier: {value!r}",
            )

    @classmethod
    def _quote_identifier(
        cls,
        value: str,
    ) -> str:
        cls._validate_identifier(value)
        return f'"{value}"'