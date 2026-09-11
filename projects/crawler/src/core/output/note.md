我建议你现在的实现顺序

不要一次把所有东西写完，按这个 Milestone 做：

M1 — Output 基础抽象
OutputItem
OutputSink
OutputEngine
OutputResolver
OutputSinkFactory
OutputError
M2 — JSONL

先实现：

Extraction
 ↓
OutputEngine
 ↓
JsonlOutputSink
 ↓
data/news.jsonl

这一步完成后，你的爬虫就真正有了完整的数据出口。

M3 — 集成 LifecycleManager
Application.start()
    ↓
JsonlOutputSink.open()

Crawler
    ↓
write()

Application.close()
    ↓
JsonlOutputSink.close()
M4 — PostgreSQL

直接接你现在已有的：

SQLAlchemy AsyncEngine
asyncpg

不要重新造数据库连接管理。

M5 — Batch / Flush

最后再做：

OutputSink.write()
OutputSink.flush()
OutputSink.close()

让 PostgreSQL 可以批量写入。

我建议下一步不要先写 PostgresOutputSink，而是先把 M1 的几个核心类定下来。 尤其是 OutputItem、OutputEngine、OutputSink、OutputConfig 和 SpiderConfig.outputs 这几个接口一旦定好，后面的 JSONL/Postgres 基本只是实现问题，而且不会破坏你现在已经跑通的 crawler pipeline。

Crawler
   ↓
Output
   ├── JSONL
   ├── PostgreSQL
   ├── Qdrant
   ├── MinIO
   └── Redis

PostgreSQL
→ structured data

MinIO
→ raw HTML / PDF / image

Qdrant
→ embeddings

Redis
→ temporary state

我特别建议你当前先不要实现这几个东西

暂时不要：

❌ OutputMiddleware
❌ OutputRetryPolicy
❌ 自动 CREATE TABLE
❌ ORM Model Generator
❌ 自动 schema inference
❌ Kafka
❌ Redis
❌ Qdrant
❌ MinIO
❌ BatchOutputEngine

先把：

JSONL
CSV
PostgreSQL

三条链路跑通。

然后下一步再做 OutputSinkFactory + OutputResolver + LifecycleManager + ApplicationContainerFactory.register_outputs()。这部分完成后，你的 Output 模块才真正接入现有 DI 架构，而不是几个孤立的 Sink 类。

write()
write()
write()
    ↓
flush()
    ↓
bulk insert

JSONL
→ flush

CSV
→ flush

Postgres
→ 第一版 no-op

write()
    ↓
buffer
    ↓
flush()
    ↓
executemany()