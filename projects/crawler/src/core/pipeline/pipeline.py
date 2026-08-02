from core.pipeline.chain import MiddlewareChain
from core.pipeline.executor import PipelineExecutor
from core.pipeline.registry import MiddlewareRegistry
from core.pipeline.typing import ContextT


class DefaultPipeline(
    PipelineExecutor[
        ContextT,
    ],

):
    def __init__(

    self,

    registry:MiddlewareRegistry[

        ContextT,

    ],

    executor:PipelineExecutor[ContextT],

):

        self._chain = MiddlewareChain(

            registry.middlewares(),

            executor,

        )

    async def execute(

        self,

        context: ContextT,

    )-> ContextT:

        return await self._chain.execute(
            context,
        )