import asyncio
from typing import Any, Literal, cast

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
from core.request.browser.interaction.model import (
    BrowserAction,
)
from core.request.browser.intervention.base import (
    HumanInterventionEngine,
)
from core.request.browser.typing import (
    BrowserActionType,
    BrowserPageState,
)
from core.request.context import RequestContext
from core.spider.config import SearchSpiderConfig


LoadState = Literal[
    "domcontentloaded",
    "load",
    "networkidle",
]

SelectorState = Literal[
    "attached",
    "detached",
    "hidden",
    "visible",
]


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
    ) -> None:
        self._inspector = inspector
        self._human_intervention = human_intervention

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
                page,
                action,
            )

            await self._handle_page_state(
                context,
                page,
            )

    # =========================================================
    # action dispatch
    # =========================================================

    async def _execute_action(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        timeout = self._timeout(
            action.timeout,
        )

        match action.type:

            case BrowserActionType.FILL:
                await self._fill(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.TYPE:
                await self._type(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.CLEAR:
                await self._clear(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.PRESS:
                await self._press(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.CLICK:
                await self._click(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.DOUBLE_CLICK:
                await self._double_click(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.HOVER:
                await self._hover(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.FOCUS:
                await self._focus(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.BLUR:
                await self._blur(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.SELECT:
                await self._select(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.CHECK:
                await self._check(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.UNCHECK:
                await self._uncheck(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.KEYBOARD_PRESS:
                await self._keyboard_press(
                    page,
                    action,
                )

            case BrowserActionType.KEYBOARD_TYPE:
                await self._keyboard_type(
                    page,
                    action,
                )

            case BrowserActionType.GOTO:
                await self._goto(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.GO_BACK:
                await self._go_back(
                    page,
                    timeout,
                )

            case BrowserActionType.GO_FORWARD:
                await self._go_forward(
                    page,
                    timeout,
                )

            case BrowserActionType.RELOAD:
                await self._reload(
                    page,
                    timeout,
                )

            case BrowserActionType.WAIT:
                await self._wait(
                    page,
                    action,
                )

            case BrowserActionType.WAIT_FOR_SELECTOR:
                await self._wait_for_selector(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.WAIT_FOR_URL:
                await self._wait_for_url(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.WAIT_FOR_LOAD_STATE:
                await self._wait_for_load_state(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.EVALUATE:
                await self._evaluate(
                    page,
                    action,
                )

            case BrowserActionType.SET_INPUT_FILES:
                await self._set_input_files(
                    page,
                    action,
                    timeout,
                )

            case BrowserActionType.SCREENSHOT:
                await self._screenshot(
                    page,
                    action,
                )

            case _:
                raise ValueError(
                    "Unsupported browser action: "
                    f"{action.type!r}",
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
    # input actions
    # =========================================================

    async def _fill(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).fill(
            self._require_value(action),
            timeout=timeout,
            force=action.force,
        )

    async def _type(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).press_sequentially(
            self._require_value(action),
            timeout=timeout,
        )

    async def _clear(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).clear(
            timeout=timeout,
            force=action.force,
        )

    async def _press(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).press(
            self._require_value(action),
            timeout=timeout,
        )

    async def _click(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).click(
            timeout=timeout,
            force=action.force,
            no_wait_after=action.no_wait_after,
        )

    async def _double_click(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).dblclick(
            timeout=timeout,
            force=action.force,
            no_wait_after=action.no_wait_after,
        )

    async def _hover(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).hover(
            timeout=timeout,
            force=action.force,
        )

    async def _focus(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).focus(
            timeout=timeout,
        )

    async def _blur(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).blur(
            timeout=timeout,
        )

    async def _select(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).select_option(
            self._require_value(action),
            timeout=timeout,
        )

    async def _check(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).check(
            timeout=timeout,
        )

    async def _uncheck(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.locator(
            self._require_selector(action),
        ).uncheck(
            timeout=timeout,
        )

    # =========================================================
    # keyboard
    # =========================================================

    async def _keyboard_press(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        await page.keyboard.press(
            self._require_value(action),
        )

    async def _keyboard_type(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        await page.keyboard.type(
            self._require_value(action),
        )

    # =========================================================
    # navigation
    # =========================================================

    async def _goto(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        url = action.url

        if url is None:
            raise ValueError(
                "goto action requires a url.",
            )

        await page.goto(
            url,
            timeout=timeout,
        )

    async def _go_back(
        self,
        page: Page,
        timeout: float | None,
    ) -> None:

        await page.go_back(
            timeout=timeout,
        )

    async def _go_forward(
        self,
        page: Page,
        timeout: float | None,
    ) -> None:

        await page.go_forward(
            timeout=timeout,
        )

    async def _reload(
        self,
        page: Page,
        timeout: float | None,
    ) -> None:

        await page.reload(
            timeout=timeout,
        )

    # =========================================================
    # waiting
    # =========================================================

    async def _wait(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        if action.timeout is None:
            raise ValueError(
                "WAIT action requires timeout.",
            )

        await page.wait_for_timeout(
            action.timeout * 1000,
        )

    async def _wait_for_selector(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        value = action.state or "visible"

        if value not in {
            "attached",
            "detached",
            "hidden",
            "visible",
        }:
            raise ValueError(
                "Invalid selector state: "
                f"{value!r}.",
            )

        await page.wait_for_selector(
            self._require_selector(action),
            timeout=timeout,
            state=cast(
                SelectorState,
                value,
            ),
        )

    async def _wait_for_url(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        await page.wait_for_url(
            self._require_value(action),
            timeout=timeout,
        )

    async def _wait_for_load_state(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        value = self._require_value(action)

        if value not in {
            "load",
            "domcontentloaded",
            "networkidle",
        }:
            raise ValueError(
                "Invalid load state: "
                f"{value!r}.",
            )

        await page.wait_for_load_state(
            cast(
                LoadState,
                value,
            ),
            timeout=timeout,
        )

    # =========================================================
    # miscellaneous
    # =========================================================

    async def _set_input_files(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        path = action.path

        if path is None:
            raise ValueError(
                "set_input_files action requires a path.",
            )

        await page.locator(
            self._require_selector(action),
        ).set_input_files(
            path,
            timeout=timeout,
        )

    async def _evaluate(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        await page.evaluate(
            self._require_value(action),
        )

    async def _screenshot(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        path = action.path

        if path is None:
            raise ValueError(
                "screenshot action requires a path.",
            )

        await page.screenshot(
            path=path,
        )

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

    # =========================================================
    # validation
    # =========================================================

    @staticmethod
    def _require_selector(
        action: BrowserAction,
    ) -> str:

        selector = action.selector

        if selector is None:
            raise ValueError(
                f"{action.type.value!r} action requires "
                "a selector.",
            )

        return selector

    @staticmethod
    def _require_value(
        action: BrowserAction,
    ) -> str:

        value = action.value

        if value is None:
            raise ValueError(
                f"{action.type.value!r} action requires "
                "a value.",
            )

        return value

    @staticmethod
    def _timeout(
        timeout: float | None,
    ) -> float | None:

        if timeout is None:
            return None

        if timeout < 0:
            raise ValueError(
                "timeout must not be negative.",
            )

        return timeout * 1000