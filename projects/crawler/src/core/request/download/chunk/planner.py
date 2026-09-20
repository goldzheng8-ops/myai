from __future__ import annotations

from abc import ABC, abstractmethod

from core.request.download.chunk.model import ChunkPlan, ChunkRange


class ChunkPlanner(ABC):

    @abstractmethod
    def plan(
        self,
        *,
        total_size: int,
        chunk_size: int,
    ) -> ChunkPlan:
        ...

class FixedChunkPlanner(
    ChunkPlanner,
):

    def plan(
        self,
        *,
        total_size: int,
        chunk_size: int,
    ) -> ChunkPlan:

        if total_size <= 0:
            raise ValueError(
                "total_size must be greater than zero.",
            )

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than zero.",
            )

        chunks: list[ChunkRange] = []

        index = 0
        start = 0

        while start < total_size:

            end = min(
                start + chunk_size - 1,
                total_size - 1,
            )

            chunks.append(
                ChunkRange(
                    index=index,
                    start=start,
                    end=end,
                ),
            )

            index += 1
            start = end + 1

        return ChunkPlan(
            total_size=total_size,
            chunks=tuple(chunks),
        )