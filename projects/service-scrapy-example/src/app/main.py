from __future__ import annotations

import asyncio
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.scrapy_service import run_scrapy_job

app = FastAPI(title="Scrapy Microservice", version="1.0.0")

_tasks: dict[str, dict[str, Any]] = {}


class CrawlTaskRequest(BaseModel):
    spider: str = Field(..., min_length=1)
    url: str | None = None


class CrawlTaskResponse(BaseModel):
    task_id: str
    status: str
    payload: dict[str, Any]


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
    task_record: dict[str, Any] = {
        "task_id": task_id,
        "status": "queued",
        "spider": payload.spider,
        "url": payload.url,
        "result": None,
    }
    _tasks[task_id] = task_record

    async def run_task() -> None:
        task_record["status"] = "running"
        try:
            result = await asyncio.to_thread(
                run_scrapy_job,
                {
                    "task_id": task_id,
                    "spider": payload.spider,
                    "url": payload.url,
                },
            )
            task_record["result"] = result
            task_record["status"] = result.get("status", "completed")
        except Exception as exc:  # pragma: no cover - defensive guard
            task_record["status"] = "failed"
            task_record["error"] = str(exc)

    asyncio.create_task(run_task())

    return {
        "task_id": task_id,
        "status": "accepted",
        "payload": {
            "spider": payload.spider,
            "url": payload.url,
            "task_status": task_record["status"],
        },
    }


@app.get("/crawl/tasks/{task_id}")
async def get_task_status(task_id: str) -> dict[str, Any]:
    task = _tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task
