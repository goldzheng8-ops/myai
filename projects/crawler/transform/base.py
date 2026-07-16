from abc import ABC, abstractmethod
from typing import Any

class TransformPlugin(ABC):

    name: str

    @abstractmethod
    def apply(
        self,
        value: Any,
        **kwargs: list[str],
    ) -> Any:
        ...