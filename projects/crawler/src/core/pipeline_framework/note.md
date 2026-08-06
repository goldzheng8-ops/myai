Pipeline
      │
      ▼
PipelinePass
      │
      ▼
PipelineStage
      │
      ▼
PipelineStep

EventResolver = Pipeline<ResolveContext> 的领域封装
LifecycleRunner = Pipeline<LifecycleContext> 的领域封装
MiddlewareChain = Pipeline<RequestContext> 的领域封装
Extractor = Pipeline<ExtractContext> 的领域封装

然后：

ResolvePipeline = Pipeline[ResolveContext]
ExecutionPipeline = Pipeline[ExecutionContext]

区别只在于：

ResolvePipeline 的 Step 是 ResolveStrategy（解析，不产生副作用）。
ExecutionPipeline 的 Step 是 Middleware/Handler（真正执行业务逻辑）。

这样，整个 Core 最终只有一套 Pipeline 基础设施，Resolver 不再重复实现 Pass、Stage、Graph，只是在语义上定义了自己的 ResolvePipeline、ResolvePass 和 ResolveStage 类型别名。这也是我认为整个框架最统一、最容易长期维护的最终方案