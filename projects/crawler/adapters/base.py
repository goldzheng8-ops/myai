from abc import ABC, abstractmethod
from typing import Any

from config.config import SelectorConfig


class ResponseAdapter(ABC):

    @abstractmethod
    def select(
        self,
        selector: SelectorConfig,
    ) -> Any:
        """
        根据 SelectorConfig 提取数据
        """
        raise NotImplementedError