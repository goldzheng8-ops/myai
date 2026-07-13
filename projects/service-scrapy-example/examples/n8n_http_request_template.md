# n8n HTTP Request 节点模板

## 1. 请求方法

- Method: POST
- URL: http://service-scrapy-example:8001/crawl/tasks

## 2. 请求体

```json
{
  "spider": "template",
  "url": "https://example.com",
  "crawler_config": {
    "template": "list",
    "request": {
      "url": "https://example.com",
      "method": "GET",
      "headers": {
        "User-Agent": "Mozilla/5.0"
      }
    },
    "browser": {
      "enabled": false
    },
    "list": {
      "selector": "article"
    },
    "pagination": {
      "enabled": false,
      "max_pages": 3
    },
    "extract": {
      "fields": {
        "title": {
          "selector": "h2::text",
          "type": "text"
        },
        "url": {
          "selector": "a::attr(href)",
          "type": "text"
        }
      }
    },
    "pipeline": {
      "deduplicate": true
    },
    "output": {
      "format": "json"
    },
    "workflow": {
      "task_name": "n8n-crawl-task",
      "ai_space_callback": "http://ai-space:8000/api/ingest"
    }
  },
  "callback_url": "http://ai-space:8000/api/ingest"
}
```

## 3. n8n 使用说明

- 把上面的 JSON 直接放进 n8n 的 HTTP Request 节点的 Body 中。
- 如果你在本机调试，可把 URL 改为 http://127.0.0.1:8001/crawl/tasks。
- 如果服务运行在 Docker 网络中，使用服务名 http://service-scrapy-example:8001/crawl/tasks。
