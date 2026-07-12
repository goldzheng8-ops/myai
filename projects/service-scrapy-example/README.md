
# 启动服务：
uvicorn app.main:app --host 0.0.0.0 --port 8001
# 提交任务：
curl -X POST http://127.0.0.1:8001/crawl/tasks \
  -H "Content-Type: application/json" \
  -d '{"spider":"example","url":"https://example.com"}'
# 查询任务状态
curl http://127.0.0.1:8001/crawl/tasks/{task_id}


###########################################################################
docker build -t service-scrapy:test .
docker run --rm -p 8001:8001 --name service-scrapy-test service-scrapy:test

docker build -t service-scrapy:test .
docker run --rm -p 8001:8001 service-scrapy:test


| 场景         | 推荐命令                                   |
| ---------- | -------------------------------------- |
| 启动 FastAPI | `uv run uvicorn app.main:app --reload` |
| 运行 Spider  | `uv run scrapy crawl <spider_name>`    |
| 运行 pytest  | `uv run pytest`                        |
| 数据库迁移      | `uv run alembic upgrade head`          |
| 执行脚本       | `uv run python xxx.py`                 |

Sprint 1
 |
 |-- Scrapy基础
 |-- Spider
 |-- Pipeline
 |-- Mongo/Postgres
 |
Sprint 2
 |
 |-- RetryMiddleware
 |-- AutoThrottle
 |-- User-Agent轮换
 |
Sprint 3
 |
 |-- rotating-proxies
 |-- Redis调度
 |-- 分布式爬虫

 Scrapy
 ↓
数据清洗
 ↓
PostgreSQL
 ↓
Embedding
 ↓
Qdrant
 ↓
LLM摘要

