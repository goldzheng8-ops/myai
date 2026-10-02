| 层                   | 职责                 | 是否可扩展 |
| ------------------- | ------------------ | ----- |
| Descriptor / Config | 描述对象，仅保存配置         | ❌     |
| Registry            | 注册与查找              | ✅     |
| Strategy / Plugin   | 单一算法实现             | ✅     |
| Engine              | 调度、选择策略            | ❌     |
| Runner              | 执行流程控制             | ❌     |
| Executor            | 生命周期、事件、Tracing、异常 | ❌     |
| Context             | 运行时状态 / 数据         | ❌     |
runtime 基础层：scope.py → cache.py → context.py
runtime 访问层：accessor.py → accessor_registry.py
runtime 解析层：config.py → strategy.py → registry.py → engine.py
pipeline 描述层：descriptor.py → pipeline.py → stage.py → pipeline_pass.py
pipeline 运行层：pass_runner.py → stage_runner.py → pipeline_runner.py
pipeline 管理层：executor.py → registry.py → manager.py → builder.py

Engine：只负责根据 ResolveConfig 选择 ResolveStrategy。
ResolveStrategy：只负责路径解析算法，不关心 Registry 的具体实现，只依赖 AccessorProvider。
AccessorProvider：只负责提供有序的 ObjectAccessor 集合，不参与解析逻辑。
ObjectAccessor：只负责“一步访问”（如 Mapping、Sequence、Attribute），永远不知道完整路径。
Config：描述插件配置（长期存在）
Context：运行时状态
Expression：描述一个需要执行/解析的表达式（值对象）
Strategy：算法
Engine：调度
Registry：注册
Provider：提供资源
Accessor：一步访问

---------------------------------------------------------------------------------------
我认为它的核心职责应该是：

保存一次执行链中动态产生的上下文变量，并为 ResolveEngine 提供作用域。

例如：

url: "{{ article.url }}"
headers:
  Authorization: "{{ auth.token }}"

或者模板执行过程中：

runtime.set("article", article)
runtime.set("page", page)
runtime.set("response", response)

这些都非常适合 RuntimeContext。

_resolver

Resolver 本身应该是共享的。

所以不要每个 RuntimeContext 创建一个新的：

ResolveEngine A
ResolveEngine B
ResolveEngine C

可以：

Application
    │
    └── ResolveEngine Singleton

然后：

RuntimeContext(
    resolver=application_resolver,
)

所以：

ResolveEngine
       ↑
       │
       ├── RuntimeContext A
       ├── RuntimeContext B
       └── RuntimeContext C

这是合理的。

九、_cache 才是最值得重新定义的

现在：

_cache: Cache[str, Any] | None

这个设计太模糊。

因为你必须回答：

这个 Cache 缓存的是什么？

如果它是：

resolve("user.name")
resolve("spider.config.xxx")

这种当前 RuntimeContext 内的表达式计算缓存：

那么它应该是 execution-scoped。

也就是说：

RuntimeContext A
    └── Cache A

RuntimeContext B
    └── Cache B

这样非常安全。

而不能：

Application
    └── RuntimeContext Singleton
            └── Cache Singleton

否则：

Request A:
resolve("session.user")
    → Alice
    → cache

Request B:
resolve("session.user")
    → cache
    → Alice   ❌
十、你的 RuntimeScope 反而很有价值

你现在：

_scopes: list[RuntimeScope]

我不会删除。

相反，我认为这个设计是有潜力的。

但我会明确它的语义：

RuntimeContext
│
├── global
│
├── execution
│
└── nested scopes

例如模板：

runtime.push(name="template")

runtime.set(
    "article",
    article,
)

...

runtime.pop()

那么：

global
    │
    └── execution
            │
            └── template
                   ├── article
                   └── page

这就是 RuntimeScope 真正应该解决的问题。

另外，你现在 RuntimeContext._scopes 的设计不要删；它非常适合承担模板/表达式执行作用域。真正需要重新定义的是它的生命周期，以及 _cache 究竟是“当前 Runtime 的 resolve cache”还是其他缓存。就你目前的代码来看，我会把它明确成 RuntimeContext-local cache，而不是全局 cache