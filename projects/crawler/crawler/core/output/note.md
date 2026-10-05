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
executemany()--
----------------------------------------------------------
我建议你不要一次把整个 Download 系统做完，而是按这个顺序：

① DownloadResult
        ↓
② RequestExecutionResult 增加 download
        ↓
③ DownloadRequestHandler 返回 DownloadResult
        ↓
④ CrawlerExecutor 能识别 download
        ↓
⑤ OutputEngine 增加 write_download()
        ↓
⑥ BinaryFileOutputSink
        ↓
⑦ DI 注册
        ↓
⑧ YAML 配置
        ↓
⑨ 实际下载图片测试

最终测试：

discovery:
  - type: image_link
    target_spider: image
    request_kind: download
    selector:
      ...
    transforms:
      - type: url_resolve

运行：

list spider
    ↓
发现 image URL
    ↓
RequestDescriptor
    kind=DOWNLOAD
    target_spider=image
    ↓
CrawlerExecutor
    ↓
RequestKindDispatcher
    ↓
DownloadRequestHandler
    ↓
RequestRunner
    ↓
HttpxDownloader
    ↓
ResponseAdapter.body
    ↓
DownloadResult
    ↓
OutputEngine
    ↓
BinaryFileOutputSink
    ↓
data/downloads/xxx.jpg

这条链跑通以后，你的框架就真正从**“网页爬虫”变成“资源获取 + 内容抽取”的通用 Crawling Runtime** 了。

**我建议现在先不要碰 MinIO/S3、文件命名模板、hash 文件名、断点下载这些东西。**先把 DownloadResult → BinaryFileOutputSink → 本地文件 这条最小闭环跑通，再扩展

Downloader
    │
    ├── Range: bytes=...
    │
    ▼
stream/chunk
    │
    ▼
temporary file
    │
    ▼
DownloadResult / DownloadArtifact

先不要为了 S3/断点下载把整个 Downloader 体系继续复杂化。

等 LocalFileStorage + S3Storage + BinaryFileOutputSink 跑通之后，再处理真正的 streaming downloader 和 multipart/resumable upload，会比较稳。

另外，如果你现在的 HttpxResponse / BrowserResponse / ScrapyResponse 已经都有 body，那么我下一步会建议我们把**DownloadResult 从 ResponseAdapter 的 body 提取逻辑统一抽出来**，避免 DownloadRequestTemplate 里针对 HTTPX / Playwright / Scrapy 写任何分支。

这样以后你的：

core.template.filters

可以增加：

basename
extension
sha256
slugify
safe_filename

例如：

filename: "{{ download.url | basename }}"

得到：

image.jpg

或者：

filename: "{{ download.body_bytes | sha256 }}.jpg"

得到：

a8f3...91c.jpg

甚至：

filename: >-
  {{ download.metadata["article_id"] }}/
  {{ download.url | basename | safe_filename }}

然后你的 core.template 可以注册一些通用 filter：

basename
extension
urlencode
lower
upper
replace
slugify
sha256

例如：

filename: "{{ download.url | basename }}"

或者：

filename: "{{ download.url | basename | lower }}"

甚至：

filename: "{{ download.url | sha256 }}.{{ download.content_type | extension }}"

outputs:
  - name: images
    type: binary_file
    directory: "./downloads"
    filename: "{{ spider }}/{{ request.url | basename }}"

或者更有用一点：

filename: "{{ download.filename or request.url | basename }}"

甚至：

filename: "{{ download.metadata.get('hash') }}.{{ download.metadata.get('extension') }}"

filename: "{{ download.body_bytes | sha256 }}.bin"

下一步我建议不要马上做 S3 并发 multipart。 先把现在这个串行 multipart 跑通，因为它正好能验证你刚刚建立的整条：

StreamingDownloadStrategy
→ BinaryStream
→ OutputEngine
→ BinaryFileOutputSink
→ Storage.write_stream

链路。等这条链路稳定以后，再单独增加 ParallelMultipartUploader，那时 S3 的并发上传和你前面的 ParallelDownloadStrategy 就可以形成两个完全独立的并发模块。