from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChunkRange:
    """
    A byte range of a downloadable resource.

    Both start and end are inclusive.
    """

    index: int
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError(
                "index must be greater than or equal to zero.",
            )

        if self.start < 0:
            raise ValueError(
                "start must be greater than or equal to zero.",
            )

        if self.end < self.start:
            raise ValueError(
                "end must be greater than or equal to start.",
            )

    @property
    def size(self) -> int:
        return self.end - self.start + 1

    def contains(self, offset: int) -> bool:
        return self.start <= offset <= self.end

@dataclass(frozen=True, slots=True)
class ChunkPlan:
    """
    Complete chunk plan for a downloadable resource.
    """

    total_size: int
    chunks: tuple[ChunkRange, ...]

    def __post_init__(self) -> None:
        if self.total_size <= 0:
            raise ValueError(
                "total_size must be greater than zero.",
            )

        if not self.chunks:
            raise ValueError(
                "chunks must not be empty.",
            )

        self._validate()

    @property
    def count(self) -> int:
        return len(self.chunks)
    @property
    def first(self) -> ChunkRange:
        if not self.chunks:
            raise RuntimeError(
                "ChunkPlan contains no chunks.",
            )

        return self.chunks[0]
    def chunk(
        self,
        index: int,
    ) -> ChunkRange:
        return self.chunks[index]

    def _validate(self) -> None:
        expected_start = 0

        for index, chunk in enumerate(self.chunks):

            if chunk.index != index:
                raise ValueError(
                    "Chunk indexes must be continuous.",
                )

            if chunk.start != expected_start:
                raise ValueError(
                    "Chunk ranges must be continuous "
                    "and must start at zero.",
                )

            expected_start = chunk.end + 1

        if expected_start != self.total_size:
            raise ValueError(
                "Chunk ranges do not cover the entire "
                "resource.",
            )


@dataclass(frozen=True, slots=True)
class ChunkDownloadResult:
    chunk: ChunkRange
    body: bytes