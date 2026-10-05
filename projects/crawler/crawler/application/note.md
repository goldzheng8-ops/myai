CrawlerApplication
ApplicationRuntime
ApplicationServices
ApplicationFactory
        │
        ├── FingerprintProvider
        │
        ├── RequestMiddleware
        │
        ├── RequestRunner
        │
        ├── ScrapyRuntime
        │      └── AsyncCrawlerRunner
        │
        ├── DownloaderRegistry
        │      ├── HTTPXDownloader
        │      ├── PlaywrightDownloader
        │      └── ScrapyDownloader
        │
        ├── ResponseAdapterFactory
        │
        ├── ExtractEngine
        │
        ├── SpiderServices
        │
        ├── SpiderRegistry
        │
        ├── SpiderExecutor
        │
        └── CrawlerRunner

        ApplicationFactory
        │
        │ assemble
        ▼
ApplicationContainer
        │
        ├── SpiderRegistry
        ├── SpiderExecutor
        ├── RequestRunner
        ├── ExtractEngine
        ├── DiscoveryEngine
        └── ...
        │
        ▼
CrawlerApplication

Phase A：Application Assembly
ApplicationContainer
ApplicationFactory
CrawlerApplication
Core services assembly
生命周期管理
Phase B：Spider Assembly
SpiderRegistry
Spider factory
Template → Spider 实例绑定
Phase C：完整运行链
HTTPX
Playwright
Scrapy
Extraction
Discovery
Result
Phase D：外部入口
CLI
FastAPI
n8n/API integration
CrawlerApplication.start()
        │
        ├── RequestRunner.start()
        ├── ScrapyRuntime.start()
        ├── PlaywrightDownloader.start()
        └── ...
        
CrawlerApplication.run()
        │
        ▼
SpiderExecutor.execute()

CrawlerApplication.close()
        │
        ├── RequestRunner.close()
        ├── ScrapyRuntime.close()
        ├── PlaywrightDownloader.close()
        └── ...

FastAPI
   │
   ▼
CrawlerApplication
   │
   ▼
ApplicationContainer
   │
   ├───────────────┐
   ▼               ▼
SpiderRegistry   SpiderExecutor
                     │
                     ▼
                SpiderServices
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
 RequestRunner   ExtractEngine  DiscoveryEngine
        │
        ▼
 DownloaderRegistry
        │
 ┌──────┼────────┐
 ▼      ▼        ▼
HTTPX  Scrapy  Playwright

┌──────────────────────────────────────┐
│              Interface               │
│          FastAPI / CLI / n8n         │
└──────────────────┬───────────────────┘
                   ↓
┌──────────────────────────────────────┐
│            Application               │
│                                      │
│ ConfigLoader                         │
│ ConfigParser                         │
│ SpiderConfigFactory                  │
│ ApplicationFactory                   │
│ Application                          │
│ Bootstrap                            │
└──────────────────┬───────────────────┘
                   ↓
┌──────────────────────────────────────┐
│                Core                  │
│                                      │
│ Spider                               │
│ Workflow                             │
│ Request                              │
│ Middleware                           │
│ Downloader                           │
│ ResponseAdapter                      │
│ Extraction                           │
│ Discovery                            │
│ Runtime                              │
└──────────────────────────────────────┘

YAML
  +
Environment Variables
  +
CLI overrides

config    = 配置转换
spider    = Spider 创建与注册
crawler   = 爬虫运行与 Scrapy Runtime
bootstrap = 全局组装与生命周期

application/
├── config/
│   ├── model.py
│   ├── parser.py
│   ├── loader.py
│   ├── factory.py
│   └── resolver.py
│
├── bootstrap/
│   ├── __init__.py
│   ├── container.py
│   ├── factory.py
│   └── lifecycle.py
│
├── spider/
│   ├── __init__.py
│   ├── resolver.py
│   ├── registry.py
│   └── factory.py
│
├── crawler/
│   ├── __init__.py
│   ├── application.py
│   ├── runner.py
│   └── service.py
│
└── runtime/
    ├── __init__.py
    └── manager.py

ProviderManager
│
├── RequestRunner
├── ExtractEngine
├── ResponseAdapterFactory
│
├── DownloaderRegistry
├── MiddlewareRegistry
│
├── SpiderRegistry
├── SpiderFactory
│
├── ScrapyRuntime
├── HTTPXDownloader
├── ScrapyDownloader
├── PlaywrightDownloader
│
└── SpiderServices

class ApplicationBootstrap:
    
    def __init__(
        self,
        file_config: ApplicationFileConfig,
    ) -> None:

        self._file_config = file_config

    def create(
        self,
    ) -> ApplicationContainer:

        spider_registry = self._create_spider_registry()

        config_factory = ApplicationConfigFactory(
            spider_registry,
        )

        config = config_factory.create(
            self._file_config,
        )

        container_factory = ApplicationContainerFactory(
            ...
        )

        return container_factory.create(
            config,
        )