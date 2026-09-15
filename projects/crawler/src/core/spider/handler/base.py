from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar

from core.output.model import OutputItem
from core.request.descriptor import RequestDescriptor
from core.request.typing import RequestKind


@dataclass(slots=True)
class RequestExecutionResult:
    item: OutputItem | None = None
    outputs: tuple[str, ...] = ()
    requests: list[RequestDescriptor] = field(
        default_factory=list,
    )
    continue_: bool = True

@dataclass(frozen=True, slots=True)
class ScheduledRequest:
    """
    Scheduled spider request.

    Keeps the descriptor and its already-computed fingerprint
    together so that fingerprint calculation is not repeated
    during request execution.
    """

    descriptor: RequestDescriptor

    fingerprint: str

@dataclass(frozen=True, slots=True)
class DownloadResult:
    url: str
    body: bytes
    filename: str | None = None
    content_type: str | None = None

class RequestKindHandler(ABC):

    # Provide a default class-level value so type checkers (Pylance)
    # can reliably see the attribute on instances and subclasses.
    kinds: ClassVar[frozenset[RequestKind]] = frozenset()
    @abstractmethod
    async def execute(
        self,
        item: ScheduledRequest,
    ) -> RequestExecutionResult:
        ...
