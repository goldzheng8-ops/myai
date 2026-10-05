from __future__ import annotations

from abc import ABC
from typing import final

from core.pipeline_legacy.pass_ import PipelinePass
from core.pipeline_legacy.runtime import PipelineRuntime
from core.pipeline_legacy.typing import ContextT, PipelineNext


class MonitoringPass(
    PipelinePass[ContextT],
    ABC,
):
    """
    Base class for observability passes.

    Template Method:

        before()

            ↓

        next_step()

            ↓

        on_success()

            ↓

        on_error()

            ↓

        after()
    """

    async def before(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ) -> None:
        ...

    async def on_success(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ) -> None:
        ...

    async def on_error(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
        exc: Exception,
    ) -> None:
        ...

    async def after(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ) -> None:
        ...

    @final
    async def process(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
        next_step: PipelineNext[ContextT],
    ) -> ContextT:

        await self.before(
            context,
            runtime,
        )

        try:

            result = await next_step(
                context,
                runtime,
            )

            await self.on_success(
                result,
                runtime,
            )

            return result

        except Exception as exc:

            await self.on_error(
                context,
                runtime,
                exc,
            )

            raise

        finally:

            await self.after(
                context,
                runtime,
            )