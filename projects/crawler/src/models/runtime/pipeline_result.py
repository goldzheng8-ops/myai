from dataclasses import dataclass, field

from core.typing.result import BaseResult


@dataclass(slots=True)
class PipelineResult(BaseResult):

    processed: int = 0

    errors: list[str] = field(default_factory=list)