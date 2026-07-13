# service-scrapy-example

## 项目目标

该服务将 Scrapy 采集能力封装为一个面向配置的微服务，支持从 n8n 或其他编排系统提交采集任务。

## 领域分层

- app: FastAPI 接口与应用服务
- domain/crawler: 爬虫配置模型、模板 Spider 与执行策略
- tests: 接口与模板行为测试

## 启动服务

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001
```

## 提交任务

### 传统 Spider

```bash
curl -X POST http://127.0.0.1:8001/crawl/tasks \
  -H "Content-Type: application/json" \
  -d '{"spider":"example","url":"https://example.com"}'
```

### 配置驱动模板 Spider

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
    }
  }'
```

## 查询任务状态

```bash
curl http://127.0.0.1:8001/crawl/tasks/{task_id}
```

## 设计说明

该微服务专注于“采集”这一件事：

1. n8n 或其他编排系统通过接口提交采集配置。
2. 服务根据 Spider 模板 + 选择器配置执行采集。
3. 输出统一 JSON 数据结构，返回给 AI-SPACE 做清洗、去重、分类、摘要和存储。

采用四类模板 Spider 进行配置驱动采集：

- TemplateListSpider: 列表页、商品页、新闻列表
- TemplateDetailSpider: 列表 → 详情
- TemplateApiSpider: JSON / AJAX 接口
- TemplateBrowserSpider: Playwright 动态页面

其他能力（翻页、登录、文件下载、代理、请求头、限速等）都通过配置项开启，而不是派生新的 Spider。

## 运行测试

```bash
uv run pytest
```

## 示例文件

- YAML 配置示例: [examples/crawl_config.yaml](examples/crawl_config.yaml)
- 标准 JSON 输出 schema: [examples/output_schema.json](examples/output_schema.json)
- AI-SPACE 回调示例: [examples/ai_space_callback_example.py](examples/ai_space_callback_example.py)
- Docker 运行示例: [examples/docker_run_examples.md](examples/docker_run_examples.md)
- n8n HTTP Request 节点模板: [examples/n8n_http_request_template.json](examples/n8n_http_request_template.json)
- n8n 使用说明: [examples/n8n_http_request_template.md](examples/n8n_http_request_template.md)
- n8n 完整工作流示例: [examples/n8n_workflow_full_example.json](examples/n8n_workflow_full_example.json)
- n8n 工作流说明: [examples/n8n_workflow_full_example.md](examples/n8n_workflow_full_example.md)
- 任务轮询示例: [examples/task_polling_example.md](examples/task_polling_example.md)
- n8n 任务轮询节点模板: [examples/n8n_task_polling_template.json](examples/n8n_task_polling_template.json)
- YAML 配置读取示例: [examples/yaml_config_loader.py](examples/yaml_config_loader.py)
- AI-SPACE 入库 schema: [examples/ai_space_ingest_schema.json](examples/ai_space_ingest_schema.json)
- AI-SPACE 回调 mock: [examples/ai_space_ingest_example.py](examples/ai_space_ingest_example.py)
- 生产流程说明: [examples/production_flow_example.md](examples/production_flow_example.md)
- 生产 API 契约: [examples/production_api_contract.md](examples/production_api_contract.md)

