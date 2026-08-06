from typing import Generic, Sequence

from core.request_pipeline.executor import PipelineExecutor
from core.request_pipeline.typing import ContextT
from core.request_pipeline.middleware import PipelineMiddleware

class MiddlewareChain(
    Generic[
        ContextT,
    ],
):
    def __init__(
        self,
        middlewares: Sequence[
            PipelineMiddleware[
                ContextT
            ]
        ],
         executor:PipelineExecutor[ContextT]
    ) -> None:

        self._middlewares = tuple(middlewares)
        self._executor = executor

    async def execute(

        self,

        context: ContextT,

    ):

        return await self._call(
            0,
            context,
        )

    async def _call(

        self,

        index:int,

        context: ContextT,

    ):

        if index >= len(
            self._middlewares,
        ):

            return await self._executor.execute(
                context,
            )

        middleware = self._middlewares[
            index
        ]

        return await middleware.process(

            context,

            lambda ctx:
                self._call(
                    index + 1,
                    ctx,
                ),

        )