然后再解决一个关键问题：Scrapy 的 reactor 启动必须是整个应用进程级的一次性初始化，而不能由每个 DefaultScrapyRuntime 自己启动/停止。

这个问题解决以后，再做 concurrency + timeout + active requests + graceful close，Scrapy 这一层就基本可以真正冻结了。
                    ┌─────────────────────┐
                    │   SpiderExecutor    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   RequestRunner     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ScrapyDownloader    │
                    └──────────┬──────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │ ScrapyRequestExecutor    │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ DefaultScrapyRuntime     │
                 │                          │
                 │ concurrency              │
                 │ timeout                  │
                 │ active tasks              │
                 │ lifecycle                │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │   AsyncCrawlerRunner     │
                 │                          │
                 │ asyncio                  │
                 │ Deferred                 │
                 │ reactor                  │
                 │ CrawlerRunner            │
                 └──────────────────────────┘


settings = Settings(
    {
        "TWISTED_REACTOR":
            "twisted.internet.asyncioreactor.AsyncioSelectorReactor",

        "TWISTED_REACTOR_ENABLED": True,

        "LOG_ENABLED": True,
    },
)
尤其要解决三个问题：
AsyncCrawlerRunner.start() 如何保证 reactor / crawler 只初始化一次；
fetch() 如何安全调用 ExecutionEngine.download_async()；
close() 如何保证 RuntimeSpider → Crawler → ExecutionEngine → AsyncCrawlerRunner 完整退出。
这一步完成以后，Scrapy 这一层才真正算“基础设施冻结”，然后再回到 SpiderExecutor → ExtractEngine → CrawlerRunner 做整条链路的集成测试。