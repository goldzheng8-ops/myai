Request

进入以后：

Request

↓

Fingerprint

↓

Duplicate Filter

↓

Proxy

↓

Cookie

↓

Session

↓

Auth

↓

Throttle

↓

Cache

↓

Retry

↓

Downloader

这些全部都是：

Request Middleware

而不是：

Downloader。

Downloader：

只负责：

Send Request

↓

Receive Response

其它什么都不应该管。

RequestEngine

职责：

RequestContext

↓

Pipeline

↓

Downloader

↓

ResponseAdapter

永远不要做：

Retry

Cookie

Proxy
Middleware

我建议保持和 Pipeline 一样。

例如：

RequestPipeline

↓

MiddlewareChain

↓

RequestMiddleware

以后：

所有：

RetryMiddleware

ProxyMiddleware

CookieMiddleware

全部：

继承：

RequestMiddleware
RequestMiddleware

例如：

class RequestMiddleware(
    Plugin,
    ABC,
):

    @abstractmethod
    async def process(
        self,
        context: RequestPipelineContext,
        next: RequestHandler,
    ) -> ResponseAdapter:
        ...

和 ASP.NET Core Pipeline 一模一样。

RequestPipelineContext

不要直接传：

SpiderContext

RequestContext

建议：

class RequestPipelineContext:

    spider: SpiderContext

    request: RequestContext

    runtime: RuntimeContext

以后：

Middleware：

统一：

操作：

context.request

context.spider
Retry

不要写：

RetryMiddleware

里面：

while ...

建议：

拆：

RetryPolicy

↓

RetryStrategy

↓

BackoffStrategy

以后：

可以：

Exponential

Fixed

Random

Fibonacci

全部插件化。

Proxy

不要：

ProxyManager

一个类。

建议：

ProxyProvider

↓

ProxySelector

↓

ProxyStrategy

例如：

Random

RoundRobin

Sticky

Country

以后：

插件。

Cookie

不要：

dict

建议：

CookieStorage

↓

CookieManager

↓

CookiePolicy

以后：

支持：

Memory

SQLite

Redis
Session

建议：

SessionStorage

↓

SessionManager

以后：

支持：

Browser Session

HTTP Session

Distributed Session
Fingerprint

非常重要。

建议：

FingerprintGenerator

↓

FingerprintStrategy

以后：

支持：

URL

URL+Body

Canonical URL

Custom
Deduplicate

建议：

DuplicateFilter

↓

Storage

以后：

支持：

Memory

BloomFilter

Redis

SQLite
Throttle

建议：

不要：

DownloadDelay

写死。

而是：

ThrottleStrategy

↓

RateLimiter

以后：

支持：

Token Bucket

Leaky Bucket

Semaphore
Cache

建议：

CacheBackend

↓

CacheManager

以后：

支持：

Memory

Redis

Disk
Auth

建议：

不要：

LoginPlugin

而是：

AuthProvider

↓

TokenProvider

以后：

支持：

Bearer

OAuth

JWT

APIKey
最后会形成整个框架
Spider
    │
    ▼
RequestEngine
    │
    ▼
RequestPipeline
    │
    ▼
RequestMiddleware
    │
    ▼
Downloader
    │
    ▼
ResponseAdapter
    │
    ▼
PipelineExecutor
    │
    ▼
ResolverEngine
    │
    ▼
ValueEngine
    │
    ▼
ExtractEngine
① Request Model（请求模型）
        │
        ▼
② Request Context（请求上下文）
        │
        ▼
③ Request Pipeline 抽象
        │
        ▼
④ Middleware 接口
        │
        ▼
⑤ Middleware Registry
        │
        ▼
⑥ Request Engine
        │
        ▼
⑦ Downloader

等这些冻结以后，再逐个实现内置中间件。

第一阶段：Request Model（先冻结）

这一层只放数据模型，不放业务逻辑。

建议冻结：

request/
│
├── context.py
├── descriptor.py
├── profile.py
├── meta.py
├── result.py
├── method.py
├── priority.py
└── state.py

例如：

RequestContext

负责一次请求运行时。

RequestDescriptor

负责描述请求本身。

RequestProfile

负责 Downloader 类型、Browser 配置等。

RequestMeta

负责 Retry、Fingerprint、DownloadDelay、Tag 等扩展信息。

这样 RequestContext 就不会越来越臃肿。

第二阶段：Request Pipeline

然后冻结：

pipeline/request/
│
├── executor.py
├── context.py
├── registry.py
├── chain.py
├── middleware.py
└── engine.py

这里和解析层保持一致。

例如：

RequestPipelineExecutor (Protocol)

↓

DefaultRequestPipeline
第三阶段：Middleware 接口

统一一个接口：

class RequestMiddleware(
    Plugin,
    ABC,
):

    async def process(
        self,
        context: RequestPipelineContext,
        next: RequestHandler,
    ) -> ResponseAdapter:
        ...

以后所有中间件全部继承它。

例如：

RetryMiddleware

ProxyMiddleware

CookieMiddleware

ThrottleMiddleware

CacheMiddleware

AuthMiddleware

完全统一。

第四阶段：逐个实现内置 Middleware

我建议按依赖关系实现，而不是按重要性。

顺序如下：

第一批（框架必须）
FingerprintMiddleware

↓

DuplicateFilterMiddleware

↓

DownloadDelayMiddleware

↓

RetryMiddleware

这四个是几乎所有爬虫都需要的。

第二批（网络）
ProxyMiddleware

↓

CookieMiddleware

↓

SessionMiddleware

↓

AuthMiddleware
第三批（性能）
CacheMiddleware

↓

CompressionMiddleware

↓

HeaderMiddleware

↓

RedirectMiddleware
为什么要这样？

因为很多中间件是有依赖关系的。

例如：

Retry

需要：

RequestMeta.retry
Proxy

需要：

Session

可能需要：

Cookie
Fingerprint

必须发生在：

Duplicate Filter

之前。

所以最好先冻结整个 Pipeline，再按顺序实现。

我还建议提前设计 Middleware 的生命周期

例如：

Request

↓

before_request

↓

Downloader

↓

after_response

↓

Extractor

↓

after_extract

所以 Middleware 不一定只有：

process(...)

以后完全可以扩展成：

class RequestMiddleware(
    Plugin,
):

    async def before_request(...):
        ...

    async def after_response(...):
        ...

    async def on_exception(...):
        ...

    async def on_finish(...):
        ...

这样：

Retry、Cache、Statistics 等中间件实现起来会非常自然。

我建议的开发路线（生产级）
① Request Model               ← 冻结
② Request Pipeline            ← 冻结
③ Middleware Interface        ← 冻结
④ Downloader Interface        ← 冻结
──────────────────────────────
⑤ FingerprintMiddleware
⑥ DuplicateMiddleware
⑦ RetryMiddleware
⑧ DelayMiddleware
⑨ ProxyMiddleware
⑩ CookieMiddleware
⑪ SessionMiddleware
⑫ CacheMiddleware
⑬ AuthMiddleware
──────────────────────────────
⑭ Scheduler
⑮ SpiderRunner