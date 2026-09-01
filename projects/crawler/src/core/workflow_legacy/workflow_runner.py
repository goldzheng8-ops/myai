from __future__ import annotations

import asyncio
from typing import Any

from core.runtime.context import RuntimeContext

from .errors import WorkflowExecutionError
from .merge import (
    DefaultWorkflowMergePolicy,
    WorkflowMergePolicy,
)
from .node import WorkflowNode
from .node_runner import NodeRunner
from .runtime import WorkflowRuntime
from .typing import (
    NodeId,
    WorkflowExecutionMode,
)


class WorkflowRunner:
    """
    Executes a WorkflowRuntime.

    WorkflowRunner is responsible only for workflow-level
    scheduling.

    Responsibilities
    ----------------
    - sequential DAG execution
    - level-based parallel execution
    - node scheduling
    - branch context isolation
    - merge-policy invocation
    - workflow execution lifecycle

    It does not:
    - execute Pipeline internals
    - implement DAG algorithms
    - implement RuntimeContext merge semantics
    - manage individual node execution details
    """

    def __init__(
        self,
        node_runner: NodeRunner | None = None,
        *,
        mode: WorkflowExecutionMode = (
            WorkflowExecutionMode.SEQUENTIAL
        ),
        merge_policy: WorkflowMergePolicy | None = None,
    ) -> None:

        self._node_runner = (
            node_runner
            if node_runner is not None
            else NodeRunner()
        )

        self._mode = mode

        self._merge_policy = (
            merge_policy
            if merge_policy is not None
            else DefaultWorkflowMergePolicy()
        )

    # =========================================================
    # Properties
    # =========================================================

    @property
    def node_runner(self) -> NodeRunner:
        return self._node_runner

    @property
    def mode(self) -> WorkflowExecutionMode:
        return self._mode

    @property
    def merge_policy(self) -> WorkflowMergePolicy:
        return self._merge_policy

    # =========================================================
    # Public API
    # =========================================================

    async def run(
        self,
        runtime: WorkflowRuntime,
    ) -> WorkflowRuntime:
        """
        Execute a workflow runtime.

        The execution mode determines whether nodes are executed
        sequentially or level-by-level in parallel.
        """

        if runtime.is_completed:
            return runtime

        if runtime.is_cancelled:
            return runtime

        if runtime.is_failed:
            return runtime

        runtime.start()

        try:

            if (
                self._mode
                is WorkflowExecutionMode.SEQUENTIAL
            ):
                await self._run_sequential(
                    runtime
                )

            elif (
                self._mode
                is WorkflowExecutionMode.PARALLEL
            ):
                await self._run_parallel(
                    runtime
                )

            else:
                raise WorkflowExecutionError(
                    "Unsupported workflow execution "
                    f"mode: {self._mode!r}"
                )

            if runtime.is_cancelled:
                return runtime

            if runtime.is_failed:
                return runtime

            runtime.complete()

            return runtime

        except asyncio.CancelledError:

            runtime.cancel()

            raise

        except Exception as exc:

            if not runtime.is_failed:
                runtime.fail(exc)

            raise

    # =========================================================
    # Sequential execution
    # =========================================================

    async def _run_sequential(
        self,
        runtime: WorkflowRuntime,
    ) -> None:
        """
        Execute workflow nodes in topological order.

        Sequential execution uses the workflow's shared
        RuntimeContext directly.
        """

        order = (
            runtime.graph.topological_sort()
        )

        for node_id in order:

            if runtime.is_cancelled:
                return

            if runtime.is_failed:
                return

            if runtime.has_completed(
                node_id
            ):
                continue

            node = runtime.graph.workflow.get_node(
                node_id
            )

            await self._run_node(
                runtime,
                node,
            )

    # =========================================================
    # Parallel execution
    # =========================================================

    async def _run_parallel(
        self,
        runtime: WorkflowRuntime,
    ) -> None:
        """
        Execute the workflow level-by-level.

        Nodes belonging to the same DAG level are independent
        according to the graph topology and may execute
        concurrently.

        Different levels remain strictly ordered.
        """

        levels = runtime.graph.levels()

        for level in levels:

            if runtime.is_cancelled:
                return

            if runtime.is_failed:
                return

            await self._run_level(
                runtime,
                level,
            )

    # =========================================================
    # Level execution
    # =========================================================

    async def _run_level(
        self,
        runtime: WorkflowRuntime,
        level: tuple[NodeId, ...],
    ) -> None:
        """
        Execute all nodes belonging to one DAG level.

        Each node receives an isolated copy of the current
        RuntimeContext.

        Contexts are merged only after every node in the level
        has completed successfully.
        """

        node_ids = tuple(
            node_id
            for node_id in level
            if not runtime.has_completed(
                node_id
            )
        )

        if not node_ids:
            return

        results = await asyncio.gather(
            *(
                self._run_isolated_node(
                    runtime,
                    node_id,
                )
                for node_id in node_ids
            ),
            return_exceptions=True,
        )

        successful: list[
            tuple[NodeId, RuntimeContext]
        ] = []

        failures: list[Exception] = []

        for node_id, result in zip(
            node_ids,
            results,
        ):

            if isinstance(
                result,
                RuntimeContext,
            ):

                successful.append(
                    (
                        node_id,
                        result,
                    )
                )

                continue

            if isinstance(
                result,
                asyncio.CancelledError,
            ):

                runtime.cancel()

                raise result

            if isinstance(
                result,
                Exception,
            ):

                failures.append(
                    self._normalize_node_exception(
                        node_id,
                        result,
                    )
                )

                continue

            failures.append(
                WorkflowExecutionError(
                    "Workflow node returned an "
                    "invalid execution result: "
                    f"{node_id!r}"
                )
            )

        if failures:

            raise self._build_level_error(
                failures
            )

        self._merge_policy.merge(
            runtime.context,
            successful,
        )

    # =========================================================
    # Node execution
    # =========================================================

    async def _run_node(
        self,
        runtime: WorkflowRuntime,
        node: WorkflowNode[Any],
    ) -> RuntimeContext:
        """
        Execute a node using the workflow's shared context.

        This is primarily used by sequential execution.
        """

        await self._node_runner.run(
            runtime,
            node.id,
            context=runtime.context,
        )

        return runtime.context

    async def _run_isolated_node(
        self,
        runtime: WorkflowRuntime,
        node_id: NodeId,
    ) -> RuntimeContext:
        """
        Execute one node using an isolated RuntimeContext.

        The original workflow context is never mutated by the
        node during parallel execution.
        """

        node = runtime.graph.workflow.get_node(
            node_id
        )

        context = runtime.context.copy()

        await self._node_runner.run(
            runtime,
            node.id,
            context=context,
        )

        return context

    # =========================================================
    # Error handling
    # =========================================================

    @staticmethod
    def _normalize_node_exception(
        node_id: NodeId,
        exception: Exception,
    ) -> Exception:

        if isinstance(
            exception,
            WorkflowExecutionError,
        ):
            return exception

        return WorkflowExecutionError(
            "Workflow node execution failed: "
            f"{node_id!r}"
        )

    @staticmethod
    def _build_level_error(
        failures: list[Exception],
    ) -> WorkflowExecutionError:

        if len(failures) == 1:
            return WorkflowExecutionError(
                str(failures[0])
            )

        return WorkflowExecutionError(
            "Multiple workflow nodes failed: "
            f"{len(failures)}"
        )