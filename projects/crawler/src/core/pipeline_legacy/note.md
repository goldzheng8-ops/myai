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

                 PipelineManager
                        │
                (管理、注册、查找)
                        │
                        ▼
                PipelineExecutor
             (整个 Pipeline 生命周期)
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
  PipelineRunner                ExecutionContext
 (Pipeline 调度)                  (运行时状态)
         │
         ▼
    StageRunner
 (Stage 调度)
         │
         ▼
     PassRunner
 (Middleware Chain)
         │
         ▼
    PipelinePass

core/
└── pipeline/
    │
    ├── descriptor.py
    │
    ├── pipeline.py
    ├── stage.py
    ├── pass.py
    │
    ├── runtime.py      ★
    │
    ├── executor.py
    ├── runner.py
    ├── stage_runner.py
    ├── pass_runner.py
    │
    ├── registry.py
    ├── manager.py
    │
    ├── errors.py
    ├── protocol.py
    ├── typing.py
    └── __init__.py

    PipelineRuntime
        │
        ├── context ─────────────► RuntimeContext
        │                              │
        │                              ├── Scope
        │                              ├── Cache
        │                              └── Resolver
        │
        ├── pipeline
        ├── stage
        ├── step
        ├── pass
        ├── cancelled
        └── exception

Runner 系列不要直接传 RuntimeContext，而是统一传 PipelineRuntime：
PipelineExecutor
        │
        ▼
PipelineRunner
        │
        ▼
StageRunner
        │
        ▼
PassRunner
async def run(
    runtime: PipelineRuntime,
) -> RuntimeContext

Descriptor
      │
      ▼
Pass
      │
      ▼
Step
      │
      ▼
Stage
      │
      ▼
Pipeline
      │
      ▼
Registry
      │
      ▼
Runtime
      │
      ▼
PassRunner
      │
      ▼
StageRunner
      │
      ▼
PipelineRunner
      │
      ▼
Executor
      │
      ▼
Manager
| 类                  | 可以依赖                    | 不能依赖                  |
| ------------------ | ----------------------- | --------------------- |
| PipelineDescriptor | 无                       | 全部                    |
| PipelinePass       | RuntimeContext          | Stage、Pipeline、Runner |
| PipelineStep       | Pass                    | Runner                |
| PipelineStage      | Step                    | Runner                |
| Pipeline           | Stage                   | Runner                |
| PipelineRegistry   | Pipeline                | Executor              |
| PipelineRuntime    | Pipeline、RuntimeContext | Runner                |
| PassRunner         | Pass、PipelineRuntime    | StageRunner           |
| StageRunner        | Stage、PassRunner        | PipelineRunner        |
| PipelineRunner     | Pipeline、StageRunner    | Executor              |
| PipelineExecutor   | PipelineRunner          | Manager               |
| PipelineManager    | Registry、Executor       | Runner                |

这是最重要的，也是我认为后续实现几乎不会遇到循环依赖的顺序：

descriptor.py（所有元数据基类）
pass.py（定义 Pass 接口）
step.py（Step 数据结构）
stage.py（Stage 数据结构）
pipeline.py（Pipeline 数据结构）
registry.py（PipelineRegistry）
runtime.py（PipelineRuntime）
pass_runner.py（执行单个 Pass）
stage_runner.py（执行一个 Stage）
pipeline_runner.py（执行整个 Pipeline）
executor.py（创建 Runtime，启动 Runner）
manager.py（管理 Pipeline，调用 Executor）

这个顺序的原则是：

先定义静态模型（Descriptor → Pass → Step → Stage → Pipeline）
再定义执行时状态（Runtime）
最后实现执行器（Runner → Executor）
Manager 永远放最后，它只是对 Registry 和 Executor 的封装

按照这个顺序实现，整个 core.pipeline_framework 基本不会出现循环导入，也与我们已经完成的 core.runtime、core.registry、core.cache 的设计风格保持一致。