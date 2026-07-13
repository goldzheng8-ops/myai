# n8n 完整工作流示例

下面这个流程把采集、等待和回调串起来：

1. HTTP Request 节点调用本服务的 /crawl/tasks 接口。
2. Wait 节点等待一段时间，给采集任务执行留出窗口。
3. HTTP Request 节点把结果回调给 AI-SPACE。

## 推荐节点配置

### 1) Submit Crawl Task
- Method: POST
- URL: http://service-scrapy-example:8001/crawl/tasks
- Body: 参考 [examples/n8n_http_request_template.json](examples/n8n_http_request_template.json)

### 2) Wait for Completion
- Amount: 5
- Unit: Seconds

### 3) AI-SPACE Callback
- Method: POST
- URL: http://ai-space:8000/api/ingest
- Body: {{$json}}

## 说明

如果你要更稳妥地等待任务完成，建议后续把任务状态查询接口接进来，再根据 task_id 做轮询。