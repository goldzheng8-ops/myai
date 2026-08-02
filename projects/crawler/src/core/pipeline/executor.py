from typing import Protocol

from .typing import ContextT


class PipelineExecutor(
    Protocol[ContextT],
):

    async def execute(
        self,
        context: ContextT,
    ) -> ContextT:
        ...