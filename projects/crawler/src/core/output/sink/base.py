from abc import ABC, abstractmethod
from typing import Generic

from core.lifecycle.protocol import LifecycleParticipant
from core.output.model import OutputItem
from core.output.typing import ConfigT


class OutputSink(
    ABC,
    LifecycleParticipant,
    Generic[ConfigT],
):

    def __init__(
        self,
        config: ConfigT,
    ) -> None:
        self._config = config

    @property
    def config(self) -> ConfigT:
        return self._config

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def write(
        self,
        item: OutputItem,
    ) -> None:
        raise NotImplementedError

    async def flush(self) -> None:
        return None

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError