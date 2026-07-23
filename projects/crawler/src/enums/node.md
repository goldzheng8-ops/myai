| DiscoveryType   | RequestKind | URL来源       | 特殊参数        |
| --------------- | ----------- | ----------- | ----------- |
| DETAIL_LINK     | DETAIL      | href        | 无           |
| NEXT_PAGE       | LIST        | href        | 无           |
| PAGE_NUMBER     | LIST        | 模板URL       | page        |
| CURSOR_API      | LIST        | API URL     | cursor      |
| GRAPHQL_CURSOR  | LIST        | GraphQL     | variables   |
| INFINITE_SCROLL | LIST        | API URL     | offset/page |
| RSS             | DETAIL/LIST | RSS XML     | 无           |
| SITEMAP         | DETAIL      | sitemap.xml | 无           |


Factory 不负责：

计算 URL
计算 page
计算 cursor
计算 GraphQL variables

这些都是 DiscoveryPlugin 的职责。

DiscoveryPlugin
        │
        │ 负责计算 URL、cursor、offset、page...
        ▼
RequestDescriptorFactory
        │
        │ 负责统一创建 Descriptor
        ▼
RequestDescriptor
        │
        ▼
RequestBuilder
        │
        ▼
RequestContext