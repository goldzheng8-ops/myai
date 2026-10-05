from __future__ import annotations

from collections import deque
from types import MappingProxyType
from typing import Generic, Mapping

from .errors import (
    WorkflowCycleError,
    WorkflowGraphStaleError,
    WorkflowValidationError,
)
from .typing import ContextT, NodeId
from .workflow import Workflow


class WorkflowGraph(
    Generic[ContextT],
):

    def __init__(
        self,
        workflow: Workflow[ContextT],
    ) -> None:

        self._workflow = workflow

        self._revision = workflow.revision

        self._adjacency = (
            self._build_adjacency()
        )

        self._reverse_adjacency = (
            self._build_reverse_adjacency()
        )

        self._frozen = False

    # ---------------------------------------------------------
    # state
    # ---------------------------------------------------------

    @property
    def workflow(
        self,
    ) -> Workflow[ContextT]:

        return self._workflow

    @property
    def revision(
        self,
    ) -> int:

        return self._revision

    @property
    def frozen(
        self,
    ) -> bool:

        return self._frozen

    def is_stale(
        self,
    ) -> bool:

        return (
            self._workflow.revision
            != self._revision
        )

    def ensure_current(
        self,
    ) -> None:

        if self.is_stale():

            raise WorkflowGraphStaleError(
                "WorkflowGraph is stale. "
                f"Graph revision="
                f"{self._revision}, "
                f"Workflow revision="
                f"{self._workflow.revision}."
            )

    def freeze(
        self,
    ) -> WorkflowGraph[ContextT]:

        self.ensure_current()

        self.validate()

        self._frozen = True

        return self

    # ---------------------------------------------------------
    # index construction
    # ---------------------------------------------------------

    def _build_adjacency(
        self,
    ) -> Mapping[
        NodeId,
        tuple[NodeId, ...],
    ]:

        adjacency: dict[
            NodeId,
            list[NodeId],
        ] = {
            node_id: []
            for node_id
            in self._workflow.node_ids()
        }

        for edge in self._workflow.edges():

            adjacency[edge.source].append(
                edge.target
            )

        return MappingProxyType(
            {
                node_id: tuple(targets)
                for node_id, targets
                in adjacency.items()
            }
        )

    def _build_reverse_adjacency(
        self,
    ) -> Mapping[
        NodeId,
        tuple[NodeId, ...],
    ]:

        reverse: dict[
            NodeId,
            list[NodeId],
        ] = {
            node_id: []
            for node_id
            in self._workflow.node_ids()
        }

        for edge in self._workflow.edges():

            reverse[edge.target].append(
                edge.source
            )

        return MappingProxyType(
            {
                node_id: tuple(sources)
                for node_id, sources
                in reverse.items()
            }
        )

    # ---------------------------------------------------------
    # graph queries
    # ---------------------------------------------------------

    def nodes(
        self,
    ) -> tuple[NodeId, ...]:

        self.ensure_current()

        return tuple(
            self._adjacency.keys()
        )

    def successors(
        self,
        node_id: NodeId,
    ) -> tuple[NodeId, ...]:

        self.ensure_current()

        try:
            return self._adjacency[node_id]

        except KeyError as exc:
            raise LookupError(
                f"Node {node_id!r} does not exist."
            ) from exc

    def predecessors(
        self,
        node_id: NodeId,
    ) -> tuple[NodeId, ...]:

        self.ensure_current()

        try:
            return (
                self._reverse_adjacency[node_id]
            )

        except KeyError as exc:
            raise LookupError(
                f"Node {node_id!r} does not exist."
            ) from exc

    def node_count(
        self,
    ) -> int:

        self.ensure_current()

        return len(self._adjacency)

    # ---------------------------------------------------------
    # entry / terminal
    # ---------------------------------------------------------

    def entry(
        self,
    ) -> NodeId:

        self.ensure_current()

        if self._workflow.entry is not None:

            return self._workflow.entry

        candidates = tuple(
            node_id
            for node_id
            in self._adjacency
            if not self._reverse_adjacency[node_id]
        )

        if len(candidates) == 1:
            return candidates[0]

        if not candidates:

            raise WorkflowValidationError(
                "Workflow has no entry node."
            )

        raise WorkflowValidationError(
            "Workflow has multiple entry "
            f"candidates: {candidates!r}."
        )

    def terminals(
        self,
    ) -> tuple[NodeId, ...]:

        self.ensure_current()

        return tuple(
            node_id
            for node_id
            in self._adjacency
            if not self._adjacency[node_id]
        )

    # ---------------------------------------------------------
    # reachability
    # ---------------------------------------------------------

    def reachable_from(
        self,
        start: NodeId,
    ) -> tuple[NodeId, ...]:

        self.ensure_current()

        if start not in self._adjacency:

            raise LookupError(
                f"Node {start!r} does not exist."
            )

        visited: set[NodeId] = set()

        queue = deque([start])

        while queue:

            current = queue.popleft()

            if current in visited:
                continue

            visited.add(current)

            queue.extend(
                target
                for target
                in self._adjacency[current]
                if target not in visited
            )

        return tuple(visited)

    # ---------------------------------------------------------
    # topology
    # ---------------------------------------------------------

    def topological_sort(
        self,
    ) -> tuple[NodeId, ...]:

        self.ensure_current()

        indegree = {
            node_id: len(
                self._reverse_adjacency[node_id]
            )
            for node_id
            in self._adjacency
        }

        queue = deque(
            node_id
            for node_id, degree
            in indegree.items()
            if degree == 0
        )

        result: list[NodeId] = []

        while queue:

            current = queue.popleft()

            result.append(current)

            for target in self._adjacency[
                current
            ]:

                indegree[target] -= 1

                if indegree[target] == 0:

                    queue.append(target)

        if len(result) != len(
            self._adjacency
        ):

            raise WorkflowCycleError(
                "Workflow contains a cycle."
            )

        return tuple(result)

    def contains_cycle(
        self,
    ) -> bool:

        try:

            self.topological_sort()

        except WorkflowCycleError:

            return True

        return False

    # ---------------------------------------------------------
    # validation
    # ---------------------------------------------------------

    def validate(
        self,
    ) -> None:

        self.ensure_current()

        if not self._adjacency:

            raise WorkflowValidationError(
                "Workflow contains no nodes."
            )

        self._validate_entry()

        self._validate_reachability()

        self._validate_terminals()

        self.topological_sort()

    def _validate_entry(
        self,
    ) -> None:

        if self._workflow.entry is not None:

            if (
                self._workflow.entry
                not in self._adjacency
            ):

                raise WorkflowValidationError(
                    "Configured entry node "
                    f"{self._workflow.entry!r} "
                    "does not exist."
                )

            return

        candidates = tuple(
            node_id
            for node_id
            in self._adjacency
            if not self._reverse_adjacency[node_id]
        )

        if len(candidates) != 1:

            raise WorkflowValidationError(
                "Workflow must have exactly "
                "one entry node. "
                f"Candidates={candidates!r}."
            )

    def _validate_reachability(
        self,
    ) -> None:

        entry = self.entry()

        reachable = set(
            self.reachable_from(entry)
        )

        unreachable = tuple(
            node_id
            for node_id
            in self._adjacency
            if node_id not in reachable
        )

        if unreachable:

            raise WorkflowValidationError(
                "Workflow contains unreachable "
                f"nodes: {unreachable!r}."
            )

    def _validate_terminals(
        self,
    ) -> None:

        terminals = self.terminals()

        if not terminals:

            raise WorkflowValidationError(
                "Workflow has no terminal node."
            )

    def is_valid(
        self,
    ) -> bool:

        try:

            self.validate()

        except WorkflowValidationError:

            return False

        return True

    # ---------------------------------------------------------
    # parallel levels
    # ---------------------------------------------------------

    def levels(
        self,
    ) -> tuple[
        tuple[NodeId, ...],
        ...
    ]:

        self.ensure_current()

        self.topological_sort()

        indegree = {
            node_id: len(
                self._reverse_adjacency[node_id]
            )
            for node_id
            in self._adjacency
        }

        current = tuple(
            node_id
            for node_id
            in self._adjacency
            if indegree[node_id] == 0
        )

        levels: list[
            tuple[NodeId, ...]
        ] = []

        while current:

            levels.append(current)

            next_level: list[NodeId] = []

            for node_id in current:

                for target in self._adjacency[
                    node_id
                ]:

                    indegree[target] -= 1

                    if indegree[target] == 0:

                        next_level.append(
                            target
                        )

            current = tuple(next_level)

        return tuple(levels)