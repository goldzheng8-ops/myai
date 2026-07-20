from abc import ABC, abstractmethod
from typing import Any, ClassVar

from adapters.base import ResponseAdapter
from selector.config.base import SelectorConfig, SelectorType


class SelectorPlugin(ABC):

    type: ClassVar[SelectorType]

    @abstractmethod
    def select(
        self,
        adapter : ResponseAdapter,
        selector: SelectorConfig
    ) -> Any:
        ...