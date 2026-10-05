from __future__ import annotations

from typing import Any

from core.pipeline_legacy.executor import PipelineExecutor
from core.runtime.context import RuntimeContext

from .errors import WorkflowNodeExecutionError
from .runtime import WorkflowRuntime
from .typing import NodeId


class NodeRunner:
    """
    Execute a single WorkflowNode.

    NodeRunner is responsible only for bridging
    WorkflowNode execution to PipelineExecutor.
    """

    def __init__(
        self,
        executor: PipelineExecutor[Any] | None = None,
    ) -> None:

        self._executor = (
            executor
            if executor is not None
            else PipelineExecutor()
        )

    @property
    def executor(
        self,
    ) -> PipelineExecutor[Any]:

        return self._executor

    async def run(
        self,
        runtime: WorkflowRuntime,
        node_id: NodeId,
        *,
        context: RuntimeContext,
    ) -> RuntimeContext:

        if runtime.is_cancelled:
            return context

        if runtime.has_completed(
            node_id,
        ):
            return context

        node = runtime.graph.workflow.get_node(
            node_id,
        )

        runtime.start_node(
            node_id,
        )

        try:

            result = await self._executor.execute(
                node.pipeline,
                context,
            )

            runtime.complete_node(
                node_id,
            )

            return result

        except Exception as exc:

            runtime.fail_node(
                node_id,
                exc,
            )

            raise WorkflowNodeExecutionError(
                node_id,
                exc,
            ) from exc