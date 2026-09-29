import asyncio
from typing import Any
import logging
from core.request.browser.exception import BrowserPageRecoveryTimeoutError
from core.request.browser.executor.registry import BrowserActionExecutorRegistry
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.intervention.registry import HumanInterventionEngineRegistry
from playwright.async_api import Page
from core.request.browser.inspector.base import (
    BrowserPageInspector,
)
from core.request.browser.interaction.base import (
    BrowserInteractionEngine,
)
from core.request.browser.interaction.context import (
    BrowserInteractionContext,
)
from core.spider.config import SearchSpiderConfig

logger=logging.getLogger(__name__)


class PlaywrightBrowserInteractionEngine(
    BrowserInteractionEngine,
):
    """
    Execute browser interaction actions against a
    Playwright page.

    Responsibilities:
    - dispatch BrowserAction
    - execute browser actions
    - inspect page state after actions
    - resolve optional human intervention
    - wait for page recovery

    This engine does not own:
    - Browser
    - BrowserContext
    - Page lifecycle
    - Request lifecycle
    - Cookie lifecycle
    """

    RECOVERY_TIMEOUT = 120.0
    RECOVERY_INTERVAL = 1.0

    def __init__(
        self,
        inspector: BrowserPageInspector,
        human_intervention_registry:
            HumanInterventionEngineRegistry,
        executor_registry:
            BrowserActionExecutorRegistry,
    ) -> None:

        self._inspector = inspector

        self._human_interventions = (
            human_intervention_registry
        )

        self._executors = executor_registry

    async def execute(
        self,
        context: BrowserInteractionContext[
            SearchSpiderConfig
        ],
    ) -> None:

        page = context.session_runtime.page

        for index, action in enumerate(
            context.config.actions,
            start=1,
        ):
            logger.info(
                "[BrowserAction] #%d type=%s",
                index,
                action.type,
            )
            await self._execute_action(
                page=page,
                action=action,
            )
            logger.info(
                "[BrowserAction] #%d completed",
                index,
            )
            await self._handle_page_state(
                context=context,
                page=page,
            )

    async def _execute_action(
        self,
        *,
        page: Page,
        action: BrowserAction,
    ) -> None:

        executor = self._executors.resolve(
            action.type,
        )

        await executor.execute(
            page,
            action,
        )

    async def _handle_page_state(
        self,
        *,
        context: BrowserInteractionContext[Any],
        page: Page,
    ) -> None:

        inspection = await self._inspector.inspect(
            page,
            context.session_runtime.page_state
        )
        logger.info(
            "[BrowserState] state=%s url=%s "
            "title=%r reason=%s",
            inspection.state.value,
            inspection.url,
            inspection.title,
            inspection.reason,
        )
        intervention = (
            self._human_interventions.resolve(
                inspection.state,
            )
        )

        if intervention is None:
            return
        logger.info(
            "[BrowserIntervention] engine=%s state=%s",
            type(intervention).__name__,
            inspection.state.value,
        )
        await intervention.intervene(
            context,
            inspection,
        )

        await self._wait_until_recovered(
            context,
            page,
        )

    async def _wait_until_recovered(
        self,
        context: BrowserInteractionContext[Any],
        page: Page,
    ) -> None:

        deadline = (
            asyncio.get_running_loop().time()
            + self.RECOVERY_TIMEOUT
        )

        while True:

            inspection = await self._inspector.inspect(
                page,
                context.session_runtime.page_state,
            )

            intervention = (
                self._human_interventions.resolve(
                    inspection.state,
                )
            )

            if intervention is None:
                return

            if (
                asyncio.get_running_loop().time()
                >= deadline
            ):
                raise BrowserPageRecoveryTimeoutError(
                    inspection=inspection,
                )

            await asyncio.sleep(
                self.RECOVERY_INTERVAL,
            )

