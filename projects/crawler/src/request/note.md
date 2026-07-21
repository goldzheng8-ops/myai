采用 Builder + Runtime Request 的设计，这样以后同时适配 Scrapy、Playwright、Requests、HTTPX、aiohttp 都不会修改核心代码
                 RequestConfig
                      │
                      ▼
              RequestBuilder
                      │
                      ▼
              RequestContext
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
 ScrapyDownloader PlaywrightDownloader RequestsDownloader
        │             │             │
        ▼             ▼             ▼
 scrapy.Request   page.goto()   requests.request()

 Builder 永远只生成统一的 RequestContext。


# 未来扩展

例如：

代理池：

ProxyMiddleware

随机 UA：

UserAgentMiddleware

AK/SK：

SignatureMiddleware

分页：

PaginationMiddleware

限速：

RateLimitMiddleware

都不用修改 Builder。

每个模块职责
① context.py

只有一个类：

RequestContext

它表示：

运行时请求对象

例如：

request.url

request.headers

request.cookies

request.meta

request.retry

以后 Downloader 永远只接收它。

② builder.py

只有一个类：

RequestBuilder


####################################

职责：

RequestConfig

↓

RequestContext

Builder 负责：

url
method
timeout
headers
params
body

它不负责：

随机UA

代理

签名

Cookie刷新

整个框架从 Request、Selector、Transform 到 Downloader 都遵循同一套 Engine + Registry + Plugin 模式，代码风格一致，后续新增任何下载器（如 aiohttp、curl_cffi、Selenium）都只需要新增一个插件即可，而无需修改已有逻辑。这也是我认为最适合作为生产级框架的整体设计。

从架构角度来看：

requests、httpx、aiohttp、playwright 都属于主动下载器（Active Downloader）：调用 download() 就能立即得到结果，非常适合放进 DownloaderEngine + Registry + Plugin。
Scrapy 属于执行框架（Execution Framework）：它自己拥有 Scheduler、Downloader、Middleware、Engine 和回调机制，不符合"调用一次返回一次"的模型。

因此，我建议：

先把 DownloaderEngine + RequestsDownloader + PlaywrightDownloader 做成生产级实现，验证整个框架设计。
等框架稳定后，再把 Scrapy 作为一种 Runner/Executor 接入，复用已经完成的 RequestBuilder、ResponseAdapter、Extractor 等模块，而不是强行塞进 DownloaderPlugin。

我认为这样既能保持架构的统一性，又不会为了兼容 Scrapy 而牺牲整个框架的设计质量。

                    Runner
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   StandardRunner          ScrapyRunner
          │                       │
          ▼                       ▼
RequestPipeline            scrapy.Engine
          │                       │
          ▼                       ▼
DownloaderEngine          scrapy.Request
          │                       │
          ▼                       ▼
DownloadResult        scrapy.Response
          │                       │
          └───────────┬───────────┘
                      ▼
               ResponseAdapter
                      ▼
                 Extractor


RequestBuilder
        │
        ▼
RequestPipeline
        │
        ▼
PlaywrightDownloader
        │
        ▼
PlaywrightResponseAdapter
        │
        ▼
SelectorEngine
        │
        ▼
TransformEngine
        │
        ▼
Extractor

scrapy.Response

↓

ScrapyResponseAdapter

↓

Extractor

✅ RequestBuilder

↓

✅ RequestPipeline

↓

✅ DownloaderEngine

↓

✅ RequestsDownloader

↓

✅ PlaywrightDownloader

↓

✅ DownloadResult

↓

✅ ResponseAdapter

↓

✅ Extractor