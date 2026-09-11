from dataclasses import dataclass, field

from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor
from core.output.model import OutputItem

@dataclass(slots=True)
class SpiderStep:
    """
    Result produced by one spider processing step.
    """

    request: RequestContext

    item: OutputItem | None = None

    outputs: tuple[str, ...] = ()

    requests: list[RequestDescriptor] = field(
        default_factory=list,
    )

    continue_: bool = True