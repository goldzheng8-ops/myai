from __future__ import annotations

from typing import Generic, Iterable

from .edge import WorkflowEdge
from .graph import WorkflowGraph
from .node import WorkflowNode
from .typing import ContextT, NodeId
from .workflow import Workflow


class WorkflowBuilder(Generic[ContextT]):
    """
    Fluent builder for Workflow definitions.

    WorkflowBuilder is responsible only for constructing the
    mutable Workflow definition.

    DAG validation and graph indexing are delegated to
    WorkflowGraph.
    """

    def __init__(
        self,
        workflow: Workflow[ContextT] | None = None,
    ) -> None:

        self._workflow = (
            workflow
            if workflow is not None
            else Workflow[ContextT](
                name="workflow",
            )
        )

    # =========================================================
    # Properties
    # =========================================================

    @property
    def workflow(
        self,
    ) -> Workflow[ContextT]:

        return self._workflow

    # =========================================================
    # Node
    # =========================================================

    def node(
        self,
        node: WorkflowNode[ContextT],
    ) -> WorkflowBuilder[ContextT]:

        self._workflow.add_node(node)

        return self

    def nodes(
        self,
        nodes: Iterable[WorkflowNode[ContextT]],
    ) -> WorkflowBuilder[ContextT]:

        for node in nodes:
            self._workflow.add_node(node)

        return self

    # =========================================================
    # Edge
    # =========================================================

    def edge(
        self,
        source: NodeId,
        target: NodeId,
    ) -> WorkflowBuilder[ContextT]:

        self._workflow.add_edge(
            WorkflowEdge(
                source=source,
                target=target,
            )
        )

        return self

    def edges(
        self,
        edges: Iterable[WorkflowEdge],
    ) -> WorkflowBuilder[ContextT]:

        for edge in edges:
            self._workflow.add_edge(edge)

        return self

    # =========================================================
    # Entry
    # =========================================================

    def entry(
        self,
        node_id: NodeId,
    ) -> WorkflowBuilder[ContextT]:

        self._workflow.set_entry(
            node_id,
        )

        return self

    # =========================================================
    # Build
    # =========================================================

    def build(
        self,
    ) -> Workflow[ContextT]:

        return self._workflow

    def build_graph(
        self,
    ) -> WorkflowGraph[ContextT]:

        graph = WorkflowGraph(
            self._workflow,
        )

        graph.validate()

        graph.freeze()

        return graph