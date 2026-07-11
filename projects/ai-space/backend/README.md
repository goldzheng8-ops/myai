| Sprint      | 功能目标            | 新技术                     |
| ----------- | --------------- | ----------------------- |
| ✅ Sprint 1  | 抓一条新闻           | FastAPI + Playwright    |
| ✅ Sprint 2  | 保存数据库           | SQLAlchemy + PostgreSQL |
| 🚀 Sprint 3 | **批量同步新闻 + 去重** | 批量 CRUD、唯一约束            |
| Sprint 4    | 定时自动同步          | n8n                     |
| Sprint 5    | AI 摘要           | OpenWebUI / LLM         |
| Sprint 6    | 多新闻源            | Scrapy + 插件化            |
| Sprint 7    | 全文抓取            | Playwright 深度抓取         |
| Sprint 8    | 向量检索            | Qdrant                  |
| Sprint 9    | MCP 接口          | MCP Server              |
| Sprint 10   | 个人 AI 办公助手      | 全流程整合                   |
sprint 4
| Task       | 内容                                                   | 难度   |
| ---------- | ---------------------------------------------------- | ---- |
| ✅ Task 4.1 | 接入 Ollama Embedding（如 `nomic-embed-text` 或 `bge-m3`） | ⭐⭐   |
| ✅ Task 4.2 | 封装 `EmbeddingService`                                | ⭐⭐   |
| ✅ Task 4.3 | 建立并初始化 Qdrant Collection                             | ⭐⭐   |
| ✅ Task 4.4 | 新闻写入 PostgreSQL 后自动写入 Qdrant                         | ⭐⭐⭐  |
| ✅ Task 4.5 | 实现 `/search` 向量检索接口                                  | ⭐⭐⭐  |
| ✅ Task 4.6 | 实现 `/chat`：RAG 检索 + 本地 LLM 回答                        | ⭐⭐⭐⭐ |


| Sprint     | 内容                                        | 是否建议现在做          |
| ---------- | ----------------------------------------- | ---------------- |
| ✅ Sprint 1 | Docker + PostgreSQL + Redis               | 完成               |
| ✅ Sprint 2 | FastAPI + SQLAlchemy                      | 完成               |
| ✅ Sprint 3 | Playwright 新闻采集                           | 完成               |
| ⭐ Sprint 4 | **n8n 定时自动同步**                            | **现在开始**         |
| ⭐ Sprint 5 | Browser Use 自动执行网页任务                      | 接着做              |
| Sprint 6   | MCP 集成（连接外部工具）                            | 之后               |
| Sprint 7   | Agent 编排（LangGraph / OpenAI Agents SDK 等） | 之后               |
| Sprint 8   | RAG + Qdrant + Embedding                  | 等硬件条件更好或使用云模型时再做 |

Task 4.1  Schedule Trigger        ✅
Task 4.2  HTTP Request            ✅
Task 4.3  IF                      ✅
-----------------------------------------
Task 4.4  Edit Fields（原 Set）
Task 4.5  Merge
Task 4.6  Loop Over Items
Task 4.7  Code(JavaScript)
Task 4.8  Error Trigger
Task 4.9  Telegram（通知）

| Sprint       | 学习目标              | 核心技术                                       |
| ------------ | ----------------- | ------------------------------------------ |
| ✅ Sprint 1-4 | 数据采集 + 自动化        | FastAPI、Playwright、SQLAlchemy、n8n          |
| 🚀 Sprint 5  | **LLM 接入与 AI 摘要** | OpenAI SDK、OpenAI Compatible API、OpenWebUI |
| Sprint 6     | **多模型切换**         | Ollama、DeepSeek、OpenAI、模型抽象层               |
| Sprint 7     | 多新闻源              | Scrapy + 插件化                               |
| Sprint 8     | 全文抓取 + AI 提炼      | Playwright 深度抓取                            |
| Sprint 9     | 向量检索              | Qdrant + Embedding                         |
| Sprint 10    | MCP + AI Agent    | MCP Server + OpenWebUI + n8n + Browser Use |
