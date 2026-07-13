from __future__ import annotations

import asyncio
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException

from app.config_loader import load_yaml_config_from_request
from app.models import RetryConfig, TaskRecord, TaskStatus
from app.persistence import get_task, init_repository, save_task
from app.retry import post_with_retry
from app.scrapy_service import run_scrapy_job
from app.schemas import CrawlTaskRequest, CrawlTaskResponse
from app.services.crawler_service import build_runner_payload

app = FastAPI(title="Scrapy Microservice", version="1.0.0")

_tasks: dict[str, dict[str, Any]] = {}


@app.on_event("startup")
async def startup() -> None:
    await init_repository()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/users/{id}")
def get_user(id: int):
    return {"id": id}

# @app.post("/news")
# def create_news(news: NewsCreate):
#     return news

@app.post("/crawl/tasks", status_code=202)
async def submit_crawl_task(payload: CrawlTaskRequest) -> CrawlTaskResponse:
    task_id = str(uuid.uuid4())
    config_from_request = load_yaml_config_from_request(payload.model_dump())
    if config_from_request:
        payload = payload.model_copy(update={"crawler_config": config_from_request})

    retry_config = payload.retry_config or RetryConfig()
    task_record = TaskRecord(
        task_id=task_id,
        status=TaskStatus.QUEUED,
        spider=payload.spider,
        url=payload.url,
        callback_url=payload.callback_url,
        result=None,
        retry_config=retry_config,
    )
    await save_task(task_record)
    _tasks[task_id] = task_record.model_dump()

    async def run_task() -> None:
        task_record.status = TaskStatus.RUNNING
        await save_task(task_record)
        _tasks[task_id] = task_record.model_dump()
        try:
            result = await asyncio.to_thread(
                run_scrapy_job,
                build_runner_payload(
                    {
                        "task_id": task_id,
                        "spider": payload.spider,
                        "url": payload.url,
                        "crawler_config": payload.crawler_config,
                        "callback_url": payload.callback_url,
                    }
                ),
            )
            task_record.result = result
            task_record.status = TaskStatus.COMPLETED if result.get("status") == "completed" else TaskStatus.FAILED
            await save_task(task_record)
            _tasks[task_id] = task_record.model_dump()

            if payload.callback_url:
                ingest_payload = {
                    "task_id": task_id,
                    "source": "crawler-service",
                    "status": task_record.status.value,
                    "payload": {
                        "spider": payload.spider,
                        "items": result.get("items", []),
                        "meta": {
                            "collected_at": result.get("collected_at"),
                            "source_url": payload.url,
                        },
                    },
                }
                try:
                    post_with_retry(
                        payload.callback_url,
                        ingest_payload,
                        retries=retry_config.retries,
                    )
                except Exception as exc:  # pragma: no cover - defensive guard
                    task_record.callback_error = str(exc)
                    await save_task(task_record)
                    _tasks[task_id] = task_record.model_dump()
        except Exception as exc:  # pragma: no cover - defensive guard
            task_record.status = TaskStatus.FAILED
            task_record.callback_error = str(exc)
            await save_task(task_record)
            _tasks[task_id] = task_record.model_dump()

    asyncio.create_task(run_task())

    return {
        "task_id": task_id,
        "status": "accepted",
        "payload": {
            "spider": payload.spider,
            "url": payload.url,
            "crawler_config": payload.crawler_config,
            "callback_url": payload.callback_url,
            "task_status": task_record.status.value,
        },
    }


@app.get("/crawl/tasks/{task_id}")
async def get_task_status(task_id: str) -> dict[str, Any]:
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task.model_dump()
