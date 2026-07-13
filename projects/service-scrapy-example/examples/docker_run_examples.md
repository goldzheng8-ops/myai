# Docker 示例

## 1. 启动服务

```bash
docker compose up --build -d
```

## 2. 提交采集任务

```bash
curl -X POST http://127.0.0.1:8001/crawl/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "spider": "template",
    "url": "https://example.com",
    "crawler_config": {
      "request": {"url": "https://example.com"},
      "list": {"selector": "article"},
      "extract": {
        "fields": {
          "title": {"selector": "h2::text", "type": "text"}
        }
      }
    },
    "callback_url": "http://host.docker.internal:8002/api/ingest"
  }'
```

## 3. 查询任务状态

```bash
curl http://127.0.0.1:8001/crawl/tasks/<task_id>
```

## 4. 启动 AI-SPACE 回调模拟服务

```bash
python examples/ai_space_callback_example.py
```
