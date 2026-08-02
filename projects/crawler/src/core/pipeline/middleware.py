from abc import ABC
from abc import abstractmethod
from typing import Generic

from .typing import ContextT
from .typing import Next


class PipelineMiddleware(
    ABC,
    Generic[ContextT],
):

    @abstractmethod
    async def process(
        self,
        context: ContextT,
        next: Next[ContextT],
    ) -> ContextT:
        ...