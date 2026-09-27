import asyncio
from typing import Any

from core.request.browser.executor.registry import BrowserActionExecutorRegistry
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
from core.request.browser.intervention.base import (
    HumanInterventionEngine,
)
from core.request.browser.typing import (
    BrowserPageState,
)
from core.request.context import RequestContext
from core.spider.config import SearchSpiderConfig


class PlaywrightBrowserInteractionEngine(
    BrowserInteractionEngine,
):
    """
    Execute browser interaction actions against a Playwright page.

    Responsibilities:
    - dispatch BrowserAction
    - execute Playwright page operations
    - normalize action timeouts
    - inspect browser page state
    - invoke human intervention when required

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
        human_intervention: HumanInterventionEngine,
        executor_registry: BrowserActionExecutorRegistry,        
    ) -> None:
        self._inspector = inspector
        self._human_intervention = human_intervention
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

            executor = self._executors.resolve(
                action.type,
            )

            await executor.execute(
                page,
                action,
            )

            await self._handle_page_state(
                context,
                page,
            )


    # =========================================================
    # response / page
    # =========================================================

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

    # =========================================================
    # page state
    # =========================================================

    async def _handle_page_state(
        self,
        context: BrowserInteractionContext[Any],
        page: Page,
    ) -> None:

        inspection = await self._inspector.inspect(
            page,
        )

        if inspection not in {
            BrowserPageState.CHALLENGE,
            BrowserPageState.CAPTCHA,
        }:
            return

        await self._human_intervention.intervene(
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

            if inspection.state == BrowserPageState.NORMAL:
                return

            if (
                asyncio.get_running_loop().time()
                >= deadline
            ):
                raise TimeoutError(
                    "Browser page did not recover "
                    "after human intervention.",
                )

            await asyncio.sleep(
                self.RECOVERY_INTERVAL,
            )

