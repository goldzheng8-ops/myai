# 任务轮询示例

## 目标

在 n8n 中提交采集任务后，使用 task_id 轮询任务状态，直到状态变为 completed 或 failed。

## 推荐流程

1. HTTP Request 提交任务，返回 task_id。
2. 分支判断 task_id 是否存在。
3. 通过 /crawl/tasks/{task_id} 轮询状态。
4. 当状态为 completed 时，继续把结果回调给 AI-SPACE。

## 轮询接口

```http
GET /crawl/tasks/{task_id}
```

## 示例响应

```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "spider": "template",
  "result": {
    "status": "completed",
    "items": [
      {
        "title": "Example",
        "url": "https://example.com"
      }
    ]
  }
}
```
