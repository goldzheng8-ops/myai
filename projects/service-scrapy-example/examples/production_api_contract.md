# Production API Contract

## 1. Submit crawl task

POST /crawl/tasks

### Request body

```json
{
  "spider": "template",
  "url": "https://example.com",
  "crawler_config": {
    "request": {"url": "https://example.com"}
  },
  "callback_url": "http://ai-space:8000/api/ingest",
  "retry_config": {
    "enabled": true,
    "retries": 3,
    "delay_seconds": 1.0,
    "timeout_seconds": 10.0
  }
}
```

### Response

```json
{
  "task_id": "uuid",
  "status": "accepted",
  "payload": {
    "spider": "template",
    "task_status": "queued"
  }
}
```

## 2. Query task status

GET /crawl/tasks/{task_id}

### Response

```json
{
  "task_id": "uuid",
  "status": "completed",
  "spider": "template",
  "callback_url": "http://ai-space:8000/api/ingest",
  "result": {
    "status": "completed",
    "items": []
  }
}
```
