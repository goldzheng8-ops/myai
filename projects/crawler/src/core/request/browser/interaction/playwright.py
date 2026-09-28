import asyncio
from typing import Any

from core.request.browser.exception import BrowserPageRecoveryTimeoutError
from core.request.browser.executor.registry import BrowserActionExecutorRegistry
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.intervention.registry import HumanInterventionEngineRegistry
from playwright.async_api import Page

from core.extraction.response.playwright import (
    PlaywrightResponseAdapter,
)
from core.request.browser.inspector.base import (
    BrowserPageInspector,
)
from core.request.browser.interaction.base import (
    BrowserInteractionEngine,
)
from core.request.browser.interaction.context import (
    BrowserInteractionContext,
)
from core.request.context import RequestContext
from core.spider.config import SearchSpiderConfig


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

        response = self._get_response(
            context.request,
        )

        page = response.page

        for action in context.config.actions:

            await self._execute_action(
                page=page,
                action=action,
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
        )

        intervention = (
            self._human_interventions.resolve(
                inspection.state,
            )
        )

        if intervention is None:
            return

        await intervention.intervene(
            context,
            inspection,
        )

        await self._wait_until_recovered(
            page,
        )

    async def _wait_until_recovered(
        self,
        page: Page,
    ) -> None:

        deadline = (
            asyncio.get_running_loop().time()
            + self.RECOVERY_TIMEOUT
        )

        while True:

            inspection = await self._inspector.inspect(
                page,
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

    @staticmethod
    def _get_response(
        request: RequestContext,
    ) -> PlaywrightResponseAdapter:

        result = request.result

        if result is None:
            raise RuntimeError(
                "Browser interaction requires "
                "a completed request result.",
            )

        response = result.response

        if not isinstance(
            response,
            PlaywrightResponseAdapter,
        ):
            raise TypeError(
                "Browser interaction requires a "
                "PlaywrightResponseAdapter, got "
                f"{type(response).__name__}.",
            )

        return response