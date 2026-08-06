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