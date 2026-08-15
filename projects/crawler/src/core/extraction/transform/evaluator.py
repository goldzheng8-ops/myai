from typing import Any, Protocol, Sequence

from core.extraction.transform.config import TransformConfig



class TransformExecutor(Protocol):

    def transform(
        self,
        value: Any,
        configs: Sequence[TransformConfig],
    ) -> Any:
        ...