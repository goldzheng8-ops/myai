from __future__ import annotations

from collections import defaultdict, deque
from typing import TYPE_CHECKING, Any, Iterator

from core.pipeline_framework.stage import PipelineStage

from .errors import PipelineGraphCycleError

if TYPE_CHECKING:
    from .stage import PipelineStage


class PipelineGraph:
    def __init__(self, name: str | None = None) -> None:
        self.name = name or "pipeline_graph"
        self._stages: dict[str, PipelineStage[Any]] = {}
        self._edges: dict[str, list[str]] = defaultdict(list)

    def __contains__(self, stage_name: str) -> bool:
        return stage_name in self._stages

    def contains(self, stage_name: str) -> bool:
        return stage_name in self._stages

    def add_stage(self, stage: PipelineStage[Any]) -> "PipelineGraph":
        if stage.name in self._stages:
            raise ValueError(f"Stage {stage.name!r} is already registered.")
        self._stages[stage.name] = stage
        self._edges.setdefault(stage.name, [])
        return self

    def add(self, stage: PipelineStage[Any]) -> "PipelineGraph":
        return self.add_stage(stage)

    def connect(self, source: str, target: str) -> "PipelineGraph":
        if source not in self._stages:
            raise KeyError(f"Source stage {source!r} is not registered.")
        if target not in self._stages:
            raise KeyError(f"Target stage {target!r} is not registered.")
        if target not in self._edges[source]:
            self._edges[source].append(target)
        return self

    def neighbors(self, stage_name: str) -> tuple[str, ...]:
        return tuple(self._edges.get(stage_name, ()))

    def topological_order(self) -> list[str]:
        indegree = {name: 0 for name in self._stages}
        adjacency: dict[str, list[str]] = {name: [] for name in self._stages}

        for source, targets in self._edges.items():
            for target in targets:
                adjacency.setdefault(source, []).append(target)
                indegree[target] = indegree.get(target, 0) + 1

        queue = deque(
            name for name in self._stages if indegree.get(name, 0) == 0
        )
        order: list[str] = []

        while queue:
            current = queue.popleft()
            order.append(current)
            for neighbor in adjacency.get(current, ()):
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self._stages):
            raise PipelineGraphCycleError("Pipeline graph contains a cycle.")

        return order

    def stages(self) -> tuple[PipelineStage[Any], ...]:
        return tuple(self._stages.values())

    def stage_names(self) -> tuple[str, ...]:
        return tuple(self._stages)

    def __iter__(self) -> Iterator[tuple[str, PipelineStage[Any]]]:
        return iter(self._stages.items())
