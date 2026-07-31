from typing import Any, Protocol, Sequence

from config.transform.base import TransformConfig



class TransformExecutor(Protocol):

    def transform(
        self,
        value: Any,
        configs: Sequence[TransformConfig],
    ) -> Any:
        ...