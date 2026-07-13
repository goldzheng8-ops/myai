| 模板                        | 覆盖场景             | 是否需要新 Spider |
| ------------------------- | ---------------- | ------------ |
| **TemplateListSpider**    | 列表页、商品页、新闻列表     | 否            |
| **TemplateDetailSpider**  | 列表 → 详情          | 否            |
| **TemplateApiSpider**     | JSON API、AJAX 接口 | 否            |
| **TemplateBrowserSpider** | Playwright 动态页面  | 否            |
其余能力（翻页、登录、下载文件、代理、请求头、限速等）都通过配置项开启，而不是派生新的 Spider。
n8n
    │
    ▼
填写采集配置（URL、CSS/XPath、是否 Playwright、翻页规则等）
    │
    ▼
Crawler Service
    ├── TemplateListSpider
    ├── TemplateDetailSpider
    ├── TemplateApiSpider
    └── TemplateBrowserSpider
    │
    ▼
统一输出 JSON
    │
    ▼
AI-SPACE（LLM 清洗、去重、分类、摘要、向量化）
    │
    ▼
PostgreSQL / Qdrant
这样以后新增一个采集任务，通常只需要新增一份 YAML 或 JSON 配置，而不是再写一个新的 Spider。这也是许多成熟爬虫平台采用的设计思路，维护成本和扩展性都会更好。

CrawlerConfig
├── request        # URL、Headers、Cookies、代理、超时
├── browser        # 是否使用 Playwright、等待策略、滚动、点击
├── list           # 列表节点定位
├── detail         # 详情页配置（可选）
├── pagination     # 翻页策略
├── extract        # 字段提取与数据转换
├── pipeline       # 去重、图片下载、文件下载等处理
├── output         # 输出格式或回调方式
└── workflow       # 调度、任务信息、AI-SPACE 回调

             CrawlerConfig（统一 DSL）
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ScrapyExecutor PlaywrightExecutor ApiExecutor
        │             │             │
        └─────────────┼─────────────┘
                      │
                Standard JSON
                      │
                  AI-SPACE