# CrawlerConfig

# Extractor

# SelectorEngine

# TransformEngine

# RequestFactory

# PaginationEngine

# TemplateListSpider

class TemplateListSpider:

    parse():

        nodes = selector.select(...)

        for node in nodes:

            yield extractor.extract(node)

        yield pager.next(...)

# TemplateDetailSpider

parse()

↓

得到URL

↓

follow

↓

extractor.extract()

# TemplateBrowserSpider
Request

↓

Playwright

↓

parse()

↓

extractor

# CrawlerRunner

FastAPI

↓

收到CrawlerConfig

↓

选择Spider

↓

启动CrawlerProcess

↓

返回JSON


crawler/
│
├── config/
│
│   crawler_config.py
│
├── selector/
│
│   selector_engine.py
│
├── extractor/
│
│   extractor.py
│
│   transform_engine.py
│
├── request/
│
│   request_factory.py
│
├── pagination/
│
│   pagination_engine.py
│
├── spiders/
│
│   template_list.py
│
│   template_detail.py
│
│   template_api.py
│
│   template_browser.py
│
├── runner/
│
│   crawler_runner.py
│
└── api/

因为以后：

新增：

Playwright

不用改 Extractor。

新增：

XPath

不用改 Spider。

新增：

JSONPath

不用改 Spider。

新增：

replace

不用改 Spider。

新增：

代理池

不用改 Spider。

Spider 永远只负责：
Request

↓

Response

↓

Selector

↓

Extractor

↓

Yield
##############################################
① CrawlerConfig                ✅ 已完成

↓

② SelectorEngine              ⭐⭐⭐⭐⭐

↓

③ TransformEngine             ⭐⭐⭐⭐⭐

↓

④ Extractor                   ⭐⭐⭐⭐⭐

↓

⑤ RequestFactory              ⭐⭐⭐⭐

↓

⑥ PaginationEngine            ⭐⭐⭐⭐

↓

⑦ TemplateListSpider          ⭐⭐⭐

↓

⑧ TemplateDetailSpider        ⭐⭐⭐

↓

⑨ TemplateApiSpider           ⭐⭐

↓

⑩ TemplateBrowserSpider       ⭐⭐

↓

⑪ CrawlerRunner               ⭐⭐⭐⭐⭐

↓

⑫ FastAPI接口                 ⭐⭐⭐⭐⭐

↓

⑬ n8n调用                     ⭐⭐⭐⭐⭐
我建议我们的实现顺序

不要一次性把所有功能做完，而是采用迭代开发：

第一版（MVP）
✅ SelectorEngine
✅ XPathHandler
✅ CSSHandler
✅ 支持 many
✅ 支持 default
第二版
RegexHandler
required
attr
完善异常处理
第三版
JSONPath / JMESPath
嵌套选择器
链式 Selector
Playwright 适配

很好，这也是我实际开发时采用的顺序。我们先让 XPath 跑起来，再扩展 CSS、Regex。

不过，在开始写代码之前，我想先调整一下我们之前的设计，因为有一个地方如果现在不改，以后支持 Playwright、BeautifulSoup、JSON 时会比较痛苦。

crawler-framework/
│
├── config/                    # 配置模型(Pydantic)
│   ├── crawler.py
│   ├── request.py
│   ├── browser.py
│   ├── list.py
│   ├── detail.py
│   ├── pipeline.py
│   ├── workflow.py
│   ├── output.py
│   ├── discovery.py
│   ├── selector.py
│   ├── transform.py
│   └── pagination.py
│
├── models/                    # 运行时对象(dataclass)
│   ├── request_context.py
│   ├── response_context.py
│   ├── discovery_item.py
│   ├── discovery_result.py
│   ├── extract_result.py
│   ├── pipeline_result.py
│   └── download_result.py
│
├── enums/
│   ├── request_kind.py
│   ├── discovery_type.py
│   ├── downloader_type.py
│   ├── response_format.py
│   ├── http_method.py
│   └── spider_template.py
│
├── profile/
│   └── request_profile.py
│
├── builder/
│   └── request_builder.py
│
├── downloader/
│   ├── base.py
│   ├── registry.py
│   ├── factory.py
│   ├── requests.py
│   ├── playwright.py
│   ├── scrapy.py
│   └── selenium.py
│
├── adapters/
│   ├── base.py
│   ├── requests.py
│   ├── playwright.py
│   ├── scrapy.py
│   └── bs4.py
│
├── extractor/
│   ├── engine.py
│   ├── result.py
│   │
│   ├── selector/
│   │   ├── engine.py
│   │   ├── registry.py
│   │   ├── base.py
│   │   ├── css.py
│   │   ├── xpath.py
│   │   ├── regex.py
│   │   └── jsonpath.py
│   │
│   └── transform/
│       ├── engine.py
│       ├── registry.py
│       ├── base.py
│       ├── regex.py
│       ├── strip.py
│       ├── upper.py
│       ├── lower.py
│       └── date.py
│
├── discovery/
│   ├── engine.py
│   ├── registry.py
│   ├── base.py
│   ├── detail.py
│   ├── next_page.py
│   ├── page_number.py
│   ├── cursor_api.py
│   └── infinite_scroll.py
│
├── scheduler/
│   ├── engine.py
│   ├── queue.py
│   ├── duplicate.py
│   └── priority.py
│
├── pipeline/
│   ├── engine.py
│   ├── registry.py
│   ├── base.py
│   ├── database.py
│   ├── file.py
│   └── webhook.py
│
├── runner/
│   ├── spider_runner.py
│   ├── workflow_runner.py
│   └── scheduler_runner.py
│
├── registry/
│   └── plugin_registry.py
│
└── utils/


crawler/
│
├── config/
│   ├── spider.py          # SpiderConfig
│   ├── request.py         # RequestConfig
│   ├── browser.py
│   ├── list.py
│   ├── detail.py
│   ├── discovery.py
│   ├── selector.py
│   ├── transform.py
│   ├── pipeline.py
│   ├── workflow.py
│   └── output.py
│
├── runtime/
│   ├── spider_context.py
│   ├── request_context.py
│   ├── request_profile.py
│   ├── discovery_item.py
│   ├── discovery_result.py
│   ├── download_result.py
│   ├── extract_result.py
│   └── pipeline_result.py
│
├── enums/
│   ├── request_kind.py
│   ├── discovery_type.py
│   ├── downloader_type.py
│   ├── response_format.py
│   ├── http_method.py
│   └── spider_template.py
│
├── request/
│   └── builder.py
│
├── downloader/
├── adapters/
├── extractor/
├── discovery/
├── scheduler/
├── pipeline/
├── registry/
├── runner/
└── utils/

                SpiderRunner
                      │
                      ▼
              RequestBuilder
                      │
                      ▼
               RequestContext
                      │
          ┌───────────┼─────────────┐
          ▼           ▼             ▼
      Scheduler   DownloaderFactory ExtractorFactory
          │           │             │
          │           │             │
     RequestKind DownloaderType ResponseFormat

 #   SpiderContext
│
├── config
├── state
├── session
├── cache
└── stats

# RequestDescriptor

url

method

headers

params

body

kind

profile

priority

meta

# RequestContext

spider

request

kind

profile

meta

# Builder：
SpiderContext
        +
Parent RequestContext
        +
RequestDescriptor

↓

RequestContext


request/

│

├── builder.py

├── context.py

├── descriptor.py

├── profile.py

└── merge.py（可选）