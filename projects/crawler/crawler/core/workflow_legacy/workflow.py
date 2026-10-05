from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic

from .descriptor import WorkflowDescriptor
from .edge import WorkflowEdge
from .node import WorkflowNode
from .typing import ContextT, NodeId


@dataclass(slots=True)
class Workflow(
    WorkflowDescriptor,
    Generic[ContextT],
):
    _revision: int = 0

    _nodes: dict[
        NodeId,
        WorkflowNode[ContextT],
    ] = field(
        default_factory=dict,
    )

    _edges: list[
        WorkflowEdge
    ] = field(
        default_factory=list,
    )

    entry: NodeId | None = None

    @property
    def revision(self) -> int:
        return self._revision

    # ---------------------------------------------------------
    # nodes
    # ---------------------------------------------------------

    def add_node(
        self,
        node: WorkflowNode[ContextT],
    ) -> None:

        if node.id in self._nodes:
            raise ValueError(
                f"Node {node.id!r} already exists."
            )

        self._nodes[node.id] = node
        self._revision += 1

    def get_node(
        self,
        node_id: NodeId,
    ) -> WorkflowNode[ContextT]:

        try:
            return self._nodes[node_id]

        except KeyError as exc:
            raise LookupError(
                f"Node {node_id!r} is not registered."
            ) from exc

    def try_get_node(
        self,
        node_id: NodeId,
    ) -> WorkflowNode[ContextT] | None:

        return self._nodes.get(node_id)

    def contains_node(
        self,
        node_id: NodeId,
    ) -> bool:

        return node_id in self._nodes

    def node_ids(
        self,
    ) -> tuple[NodeId, ...]:

        return tuple(self._nodes)

    def node_count(
        self,
    ) -> int:

        return len(self._nodes)

    # ---------------------------------------------------------
    # edges
    # ---------------------------------------------------------

    def add_edge(
        self,
        edge: WorkflowEdge,
    ) -> None:

        if edge.source not in self._nodes:
            raise LookupError(
                f"Source node "
                f"{edge.source!r} does not exist."
            )

        if edge.target not in self._nodes:
            raise LookupError(
                f"Target node "
                f"{edge.target!r} does not exist."
            )

        self._edges.append(edge)
        self._revision += 1

    def edges(
        self,
    ) -> tuple[WorkflowEdge, ...]:

        return tuple(self._edges)

    def edge_count(
        self,
    ) -> int:

        return len(self._edges)

    def remove_edge(
        self,
        source: NodeId,
        target: NodeId,
    ) -> bool:

        for index, edge in enumerate(
            self._edges
        ):

            if (
                edge.source == source
                and edge.target == target
            ):

                del self._edges[index]
                self._revision += 1

                return True

        return False

    # ---------------------------------------------------------
    # graph queries
    # ---------------------------------------------------------

    def successors(
        self,
        node_id: NodeId,
    ) -> tuple[NodeId, ...]:

        if node_id not in self._nodes:
            raise LookupError(
                f"Node {node_id!r} does not exist."
            )

        return tuple(
            edge.target
            for edge in self._edges
            if edge.source == node_id
        )

    def predecessors(
        self,
        node_id: NodeId,
    ) -> tuple[NodeId, ...]:

        if node_id not in self._nodes:
            raise LookupError(
                f"Node {node_id!r} does not exist."
            )

        return tuple(
            edge.source
            for edge in self._edges
            if edge.target == node_id
        )

    # ---------------------------------------------------------
    # entry
    # ---------------------------------------------------------

    def set_entry(
        self,
        node_id: NodeId,
    ) -> None:

        if node_id not in self._nodes:
            raise LookupError(
                f"Entry node "
                f"{node_id!r} does not exist."
            )

        self.entry = node_id
        self._revision += 1

    def find_entry_candidates(
        self,
    ) -> tuple[NodeId, ...]:

        targets = {
            edge.target
            for edge in self._edges
        }

        return tuple(
            node_id
            for node_id in self._nodes
            if node_id not in targets
        )

    def find_terminal_candidates(
        self,
    ) -> tuple[NodeId, ...]:

        sources = {
            edge.source
            for edge in self._edges
        }

        return tuple(
            node_id
            for node_id in self._nodes
            if node_id not in sources
        )

    # ---------------------------------------------------------
    # mutation
    # ---------------------------------------------------------

    def remove_node(
        self,
        node_id: NodeId,
    ) -> WorkflowNode[ContextT]:

        try:
            node = self._nodes.pop(node_id)

        except KeyError as exc:
            raise LookupError(
                f"Node {node_id!r} does not exist."
            ) from exc

        self._edges = [
            edge
            for edge in self._edges
            if (
                edge.source != node_id
                and edge.target != node_id
            )
        ]

        if self.entry == node_id:
            self.entry = None
            
        self._revision += 1

        return node