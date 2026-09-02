from typing import Any, Protocol
from collections.abc import Sequence
from core.extraction.transform.config import TransformConfigUnion



class TransformExecutor(Protocol):

    def transform(
        self,
        value: Any,
        configs: Sequence[TransformConfigUnion],
    ) -> Any:
        ...