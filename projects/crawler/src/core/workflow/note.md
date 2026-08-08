做一轮完整的同步 DAG 执行链路测试；确认 A → B → C、分支、汇聚、异常、取消、stale graph 都正确后，再给 WorkflowRunner 增加基于 graph.levels() 的并行执行模式

                         WorkflowExecutor
                                │
                                ▼
                         WorkflowRunner
                                │
                  ┌─────────────┴──────────────┐
                  │                            │
             sequential                    parallel
                  │                            │
          topological_sort()                 levels()
                                               │
                                      ┌────────┴────────┐
                                      ▼                 ▼
                                   Node B            Node C
                                      │                 │
                                      ▼                 ▼
                                  Context B         Context C
                                      │                 │
                                      └────────┬────────┘
                                               │
                                               ▼
                                    WorkflowMergePolicy
                                               │
                                               ▼
                                    ContextMergeStrategy
                                               │
                                               ▼
                                        RuntimeContext

                    core.workflow
                         │
          ┌──────────────┴──────────────┐
          │                             │
      Definition                    Execution
          │                             │
     WorkflowBuilder                    │
          │                             │
          ▼                             ▼
      Workflow ───────────────► WorkflowGraph
          │                         │
          │                         ▼
          │                  WorkflowRuntime
          │                         │
          │                         ▼
          │                  WorkflowRunner
          │                         │
          │                         ▼
          │                    NodeRunner
          │                         │
          │                         ▼
          └────────────────► PipelineExecutor