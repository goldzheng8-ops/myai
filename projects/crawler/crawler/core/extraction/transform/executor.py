from typing import Any, Protocol
from collections.abc import Sequence
from core.extraction.transform.config import TransformConfigUnion
from core.extraction.transform.context import TransformContext



class TransformExecutor(Protocol):

    def transform(
        self,
        *,
        value: Any,
        configs: Sequence[TransformConfigUnion],
        context: TransformContext | None = None,
    ) -> Any:
        ...