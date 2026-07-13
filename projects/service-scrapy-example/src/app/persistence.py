from __future__ import annotations

import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database import Base, TaskORM, build_async_engine, build_session_factory
from app.models import RetryConfig, TaskRecord, TaskStatus


class AsyncSQLAlchemyTaskRepository:
    def __init__(self, database_url: str | None = None) -> None:
        self.engine = build_async_engine(database_url)
        self.session_factory = build_session_factory(self.engine)

    async def init(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def save(self, record: TaskRecord) -> TaskRecord:
        async with self.session_factory() as session:
            orm = await session.get(TaskORM, record.task_id)
            if orm is None:
                orm = TaskORM(task_id=record.task_id)
            orm.status = record.status.value
            orm.spider = record.spider
            orm.url = record.url
            orm.callback_url = record.callback_url
            orm.result = json.dumps(record.result) if record.result is not None else None
            orm.callback_error = record.callback_error
            orm.retry_config = json.dumps(record.retry_config.model_dump()) if record.retry_config else None
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
        return record

    async def get(self, task_id: str) -> TaskRecord | None:
        async with self.session_factory() as session:
            orm = await session.get(TaskORM, task_id)
            if orm is None:
                return None
            return TaskRecord(
                task_id=orm.task_id,
                status=TaskStatus(orm.status),
                spider=orm.spider,
                url=orm.url,
                callback_url=orm.callback_url,
                result=json.loads(orm.result) if orm.result else None,
                callback_error=orm.callback_error,
                retry_config=RetryConfig.model_validate(json.loads(orm.retry_config)) if orm.retry_config else RetryConfig(),
            )

    async def list(self) -> list[TaskRecord]:
        async with self.session_factory() as session:
            result = await session.execute(select(TaskORM))
            rows = result.scalars().all()
            return [
                TaskRecord(
                    task_id=row.task_id,
                    status=TaskStatus(row.status),
                    spider=row.spider,
                    url=row.url,
                    callback_url=row.callback_url,
                    result=json.loads(row.result) if row.result else None,
                    callback_error=row.callback_error,
                    retry_config=RetryConfig.model_validate(json.loads(row.retry_config)) if row.retry_config else RetryConfig(),
                )
                for row in rows
            ]


repository = AsyncSQLAlchemyTaskRepository()


async def init_repository() -> None:
    await repository.init()


async def save_task(record: TaskRecord) -> TaskRecord:
    return await repository.save(record)


async def get_task(task_id: str) -> TaskRecord | None:
    return await repository.get(task_id)
