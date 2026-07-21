| Engine               | 输入                               | 输出                                         | 职责            |
| -------------------- | -------------------------------- | ------------------------------------------ | ------------- |
| SelectorEngine       | ResponseAdapter                  | SelectorResult                             | 从响应中定位原始数据    |
| TransformEngine      | SelectorResult                   | TransformResult                            | 将原始数据转换为业务数据  |
| **PaginationEngine** | ResponseAdapter + RequestContext | **PaginationResult（新的 RequestContext 列表）** | 根据当前响应生成下一批请求 |

这种设计有几个优点：

职责单一：PaginationEngine 不负责下载，只负责生成下一步请求。
与 Runner 解耦：Runner 统一消费 PaginationResult.requests，放回调度队列即可。
易于扩展：无论是 HTML 的下一页链接、页码递增、API Cursor，还是 Playwright 的无限滚动，都可以通过不同插件实现，而无需修改 Engine 或 Scheduler。

这也使得你的整个爬虫框架形成了非常统一的插件架构：Downloader → Selector → Transform → Pagination，四个 Engine 的组织方式和扩展方式保持一致，后续维护和新增插件都会更加简单。

Downloader
      │
      ▼
ResponseAdapter
      │
      ├──────────────┐
      │              │
      ▼              ▼
ExtractorEngine   PaginationEngine
      │              │
      ▼              ▼
   Item         RequestContext[]
      │              │
      └──────┬───────┘
             ▼
       SchedulerRunner

如果你的目标是做一个比 Scrapy 更现代、更插件化的框架，那么可以考虑把 PaginationEngine 改名为 RequestEngine（或 RequestGeneratorEngine）。

| 插件               | 实际作用         |
| ---------------- | ------------ |
| `next_link`      | 生成下一页请求      |
| `detail_links`   | 生成详情页请求      |
| `api_cursor`     | 生成下一次 API 请求 |
| `related_pages`  | 生成关联页面请求     |
| `download_files` | 生成附件下载请求     |

这些本质上都是从当前响应生成新的 RequestContext，而不是狭义的分页。这样命名以后，整个架构会更统一：

Downloader：生成 Response
ExtractorEngine：生成 Item
RequestEngine：生成新的 RequestContext
SchedulerRunner：消费 RequestContext 并调度执行

RequestContext
      │
      ▼
Downloader
      │
      ▼
ResponseAdapter
      ├──────────────► ExtractorEngine ─────► Item
      │
      └──────────────► RequestEngine ───────► RequestContext[]
                                             │
                                             ▼
                                      SchedulerRunner