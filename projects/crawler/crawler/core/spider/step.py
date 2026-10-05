from dataclasses import dataclass, field

from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor
from core.output.model import OutputItem, DownloadArtifact

@dataclass(slots=True)
class RequestStep:
    request: RequestContext
    item: OutputItem | None = None
    download: DownloadArtifact | None = None
    outputs: tuple[str, ...] = ()
    requests: list[RequestDescriptor] = field(
        default_factory=list,
    )
    continue_: bool = True