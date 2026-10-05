from __future__ import annotations

from typing import Any

from core.runtime.context import RuntimeContext

from .graph import WorkflowGraph
from .runtime import WorkflowRuntime
from .workflow import Workflow
from .workflow_runner import WorkflowRunner


class WorkflowExecutor:

    def __init__(
        self,
        runner: WorkflowRunner | None = None,
    ) -> None:

        self._runner = (
            runner
            if runner is not None
            else WorkflowRunner()
        )

    @property
    def runner(self) -> WorkflowRunner:
        return self._runner

    async def execute(
        self,
        workflow: Workflow[Any],
        context: RuntimeContext,
    ) -> RuntimeContext:

        graph = WorkflowGraph(
            workflow,
        ).freeze()

        return await self.execute_graph(
            graph,
            context,
        )

    async def execute_graph(
        self,
        graph: WorkflowGraph[Any],
        context: RuntimeContext,
    ) -> RuntimeContext:

        runtime = WorkflowRuntime.create(
            graph,
            context,
        )

        await self._runner.run(
            runtime,
        )

        return runtime.context

    async def execute_runtime(
        self,
        runtime: WorkflowRuntime,
    ) -> WorkflowRuntime:

        await self._runner.run(
            runtime,
        )

        return runtime