| Event 需要     | 复用                       |
| ------------ | ------------------------ |
| 多 Handler 注册 | `MultiRegistry`          |
| Handler 提供   | `Provider`               |
| Handler 执行   | `PipelineExecutor`       |
| Context      | `RuntimeContext`         |
| 生命周期         | `Lifecycle`              |
| Handler 中间处理 | `PipelinePass`           |
| Retry        | `RetryPass`              |
| Logging      | `LoggingPass`            |
| Metrics      | `MetricsPass`            |
| Tracing      | `TracingPass`            |
| Debug        | `DebugPass`              |
| Monitoring   | `MonitoringPass`         |
| 错误体系         | Event 专属 errors + 基础错误机制 |

1. typing.py
2. event.py
3. handler.py
4. registry.py
5. provider.py
EventKey
Event
EventHandler
EventHandlerRegistration
EventRegistry
EventHandlerProvider
再实现 Dispatcher / Runner，能够最大程度避免后面再次发生 Runtime、Provider、Registry 职责互相倒置的问题