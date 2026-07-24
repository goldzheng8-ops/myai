DetailLinkDiscovery
NextPageDiscovery
PageNumberDiscovery

ApiCursorDiscovery
InfiniteScrollDiscovery

FeedDiscovery(RSS/Sitemap)

                 DiscoveryPlugin
                       │
      ┌────────────────┼───────────────┐
      │                │               │
      │                │               │
DetailLink     NextPage      PageNumber
      │
      │
ApiDiscoveryBase
      │
      ├──────────────┐
      │              │
CursorApi     InfiniteScroll


按"发现机制"而不是按"协议名称"分类：
| DiscoveryPlugin | 发现依据              |
| --------------- | ----------------- |
| DetailLink      | HTML 链接           |
| NextPage        | HTML 下一页          |
| PageNumber      | HTML 页码           |
| CursorApi       | JSON 中的 cursor    |
| InfiniteScroll  | 滚动后获取 JSON cursor |
| OffsetApi       | 请求参数递增 offset     |
| FeedDiscovery   | RSS/XML/Sitemap   |


DiscoveryPlugin
│
├── HtmlDiscoveryPlugin
│      │
│      ├── DetailLinkDiscovery
│      ├── NextPageDiscovery
│      └── PageNumberDiscovery
│
└── ApiDiscoveryPlugin
       │
       ├── CursorApiDiscovery
       ├── InfiniteScrollDiscovery
       └── OffsetApiDiscovery