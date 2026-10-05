import asyncio
from typing import Any

from core.request.browser.config import HumanInterventionConfig
from core.request.browser.exception import HumanInterventionTimeoutError
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.interaction.context import BrowserInteractionContext
from core.request.browser.intervention.base import HumanInterventionEngine
from core.request.browser.intervention.handler.base import HumanInterventionHandler


class ManualHumanInterventionEngine(
    HumanInterventionEngine,
):

    def __init__(
        self,
        handler: HumanInterventionHandler,
        config: HumanInterventionConfig | None = None,
    ) -> None:

        self._handler = handler

        self._config = (
            config
            if config is not None
            else HumanInterventionConfig()
        )

    async def intervene(
        self,
        context: BrowserInteractionContext[Any],
        inspection: BrowserPageInspection,
    ) -> None:

        timeout = self._config.timeout

        if timeout is None:
            await self._handler.wait_for_intervention(
                context,
                inspection,
            )
            return

        try:

            await asyncio.wait_for(
                self._handler.wait_for_intervention(
                    context,
                    inspection,
                ),
                timeout=timeout,
            )

        except TimeoutError as exc:

            raise HumanInterventionTimeoutError(
                inspection=inspection,
            ) from exc