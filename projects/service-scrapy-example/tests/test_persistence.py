import pytest

from app.models import RetryConfig, TaskRecord, TaskStatus
from app.persistence import AsyncSQLAlchemyTaskRepository


@pytest.mark.asyncio
async def test_sqlalchemy_repository_round_trip():
    repo = AsyncSQLAlchemyTaskRepository(database_url="sqlite+aiosqlite:///:memory:")
    await repo.init()

    record = TaskRecord(
        task_id="task-1",
        status=TaskStatus.QUEUED,
        spider="template",
        url="https://example.com",
        callback_url="https://ai-space.example/ingest",
        retry_config=RetryConfig(retries=5),
    )

    saved = await repo.save(record)
    fetched = await repo.get(saved.task_id)

    assert fetched is not None
    assert fetched.task_id == "task-1"
    assert fetched.status == TaskStatus.QUEUED
    assert fetched.retry_config.retries == 5
