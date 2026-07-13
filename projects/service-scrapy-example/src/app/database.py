from __future__ import annotations

import os
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/crawler")


class Base(DeclarativeBase):
    pass


class TaskORM(Base):
    __tablename__ = "crawl_tasks"

    task_id: Mapped[str] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(nullable=False)
    spider: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str | None]
    callback_url: Mapped[str | None]
    result: Mapped[str | None]
    callback_error: Mapped[str | None]
    retry_config: Mapped[str | None]


def build_async_engine(database_url: str | None = None) -> Any:
    return create_async_engine(database_url or DATABASE_URL, echo=False)


def build_session_factory(engine: Any) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)
