from abc import ABC, abstractmethod
from typing import Any

from adapters.base import ResponseAdapter
from selector.config.base import SelectorConfig


class SelectorPlugin(ABC):

    name: str

    @abstractmethod
    def select(
        self,
        adapter : ResponseAdapter,
        selector: SelectorConfig
    ) -> Any:
        ...