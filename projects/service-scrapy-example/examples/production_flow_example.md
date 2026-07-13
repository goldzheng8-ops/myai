# 生产可部署流程示例

## 1. n8n 提交任务

使用 [examples/n8n_http_request_template.json](examples/n8n_http_request_template.json) 提交任务。

## 2. n8n 轮询任务状态

使用 [examples/n8n_task_polling_template.json](examples/n8n_task_polling_template.json) 轮询状态。

## 3. 服务支持的输入

FastAPI 现在同时支持：

- 直接传入 crawler_config
- 传入 config_yaml
- 传入 config_file

## 4. AI-SPACE 回调

任务完成后，服务会将结果以入库格式回调到 callback_url，并在失败时重试 3 次。