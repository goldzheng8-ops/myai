from collections.abc import AsyncIterator, Mapping
from dataclasses import field,dataclass
from typing import Any


BinaryStream = AsyncIterator[bytes]

@dataclass(slots=True)
class DownloadBody:
    body_bytes: bytes | None = None
    body_stream: BinaryStream | None = None

    def __post_init__(self) -> None:
        if self.body_bytes is None and self.body_stream is None:
            raise ValueError(
                "DownloadBody must contain either "
                "bytes or stream.",
            )

        if self.body_bytes is not None and self.body_stream is not None:
            raise ValueError(
                "DownloadBody cannot contain both "
                "bytes and stream.",
            )
        
@dataclass(frozen=True, slots=True)
class OutputItem:
    data: Any
    spider: str
    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

@dataclass(slots=True)
class DownloadResult:
    url: str

    body: DownloadBody

    content_type: str | None = None
    filename: str | None = None

    headers: Mapping[str, str] = field(
        default_factory=dict,
    )

    size: int | None = None

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    async def iter_bytes(
        self,
        chunk_size: int = 64 * 1024,
    ) -> BinaryStream:
        if self.body.body_stream is not None:
            async for chunk in self.body.body_stream:
                yield chunk
            return

        if self.body.body_bytes is not None:
            for offset in range(
                0,
                len(self.body.body_bytes),
                chunk_size,
            ):
                yield self.body.body_bytes[
                    offset:offset + chunk_size
                ]
            return

        raise RuntimeError(
            "DownloadResult contains neither "
            "body_bytes nor body_stream.",
        )