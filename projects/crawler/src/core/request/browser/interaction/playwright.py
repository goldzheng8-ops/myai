from typing import Any, Literal, cast

from core.extraction.response.playwright import PlaywrightResponseAdapter
from core.request.browser.interaction.base import BrowserInteractionEngine
from core.request.browser.interaction.context import BrowserInteractionContext
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType, BrowserPageState
from core.request.context import RequestContext
from playwright.async_api import Page
from core.spider.config import SearchSpiderConfig

LoadState = Literal['domcontentloaded', 'load', 'networkidle']
SelectorState = Literal['attached', 'detached', 'hidden', 'visible']

class PlaywrightBrowserInteractionEngine(
    BrowserInteractionEngine,
):

    async def execute(
        self,
        context: BrowserInteractionContext[
            SearchSpiderConfig
        ],
    ) -> None:

        response = self._get_response(
            context.request,
        )

        page = self._get_page(
            response,
        )
        session = self._get_session(
            context.request,
        )

        browser = await self._browser_runtime_manager.get_or_create(
            session,
        )

        page = browser.page
        for action in context.config.actions:

            print(
                "\n========== ACTION =========="
            )
            print("type:", action.type)
            print("selector:", action.selector)
            print("value:", action.value)            
            await self._execute_action(
                page,
                action,
            )
            await self._handle_page_state(
                context,
                page,
            )

            print("URL:", page.url)
            print("TITLE:", await page.title())

            if action.type == BrowserActionType.CLICK:
                print(
                    "#links count:",
                    await page.locator("#links").count(),
                )
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
                print(
                    "before click:",
                    page.url,
                )
                await self._click(
                    page,
                    action,
                    timeout,
                )
                print(
                    "after click:",
                    page.url,
                )

                print(
                    "search q:",
                    await page.locator(
                        'input[name="q"]'
                    ).input_value(),
                )
                print(await page.content())
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
                await page.go_back(
                    timeout=timeout,
                )

            case BrowserActionType.GO_FORWARD:
                await page.go_forward(
                    timeout=timeout,
                )

            case BrowserActionType.RELOAD:
                await page.reload(
                    timeout=timeout,
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
                    f"Unsupported browser action: "
                    f"{action.type!r}",
                )

    def _get_response(
        self,
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

    def _get_page(
        self,
        response: PlaywrightResponseAdapter,
    ) -> Page:

        page = response.page

        return page

    async def _fill(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        selector = self._require_selector(action)
        value = self._require_value(action)

        await page.locator(selector).fill(
            value,
            timeout=timeout,
            force=action.force,
        )

    async def _type(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        selector = self._require_selector(action)
        value = self._require_value(action)

        await page.locator(selector).press_sequentially(
            value,
            timeout=timeout,
        )

    async def _clear(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        selector = self._require_selector(action)

        await page.locator(selector).clear(
            timeout=timeout,
            force=action.force,
        )

    async def _click(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        selector = self._require_selector(action)

        await page.locator(selector).click(
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

        selector = self._require_selector(action)

        await page.locator(selector).dblclick(
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

        selector = self._require_selector(action)

        await page.locator(selector).hover(
            timeout=timeout,
            force=action.force,
        )

    async def _focus(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        selector = self._require_selector(action)

        await page.locator(selector).focus(
            timeout=timeout,
        )

    async def _blur(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        selector = self._require_selector(action)

        await page.locator(selector).blur(
            timeout=timeout,
        )

    async def _select(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        selector = self._require_selector(action)
        value = self._require_value(action)

        await page.locator(selector).select_option(
            value,
            timeout=timeout,
        )
    async def _check(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        selector = self._require_selector(
            action,
        )

        await page.locator(
            selector,
        ).check(
            timeout=timeout,
        )

    async def _uncheck(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        selector = self._require_selector(
            action,
        )

        await page.locator(
            selector,
        ).uncheck(
            timeout=timeout,
        )

    async def _keyboard_press(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        value = self._require_value(action)

        await page.keyboard.press(
            value,
        )

    async def _keyboard_type(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        value = self._require_value(action)

        await page.keyboard.type(
            value,
        )

    async def _press(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        selector = self._require_selector(action)
        value = self._require_value(action)

        await page.locator(selector).press(
            value,
            timeout=timeout,
        )

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

        selector = self._require_selector(action)

        value= action.state or "visible"
        
        if value not in {
            "attached",
            "detached",
            "hidden",
            "visible",
        }:
            raise ValueError(
                "Invalid load state: "
                f"{value!r}",
            )

        load_state = cast(
            SelectorState,
            value,
        ) 
        await page.wait_for_selector(
            selector,
            timeout=timeout,
            state=load_state,
        )

    async def _wait_for_url(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        value = self._require_value(action)

        await page.wait_for_url(
            value,
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
                f"{value!r}",
            )

        load_state = cast(
            LoadState,
            value,
        )
        await page.wait_for_load_state(
            load_state,  
            timeout=timeout,
        )

    async def _set_input_files(
        self,
        page: Page,
        action: BrowserAction,
        timeout: float | None,
    ) -> None:

        selector = self._require_selector(action)

        path = action.path

        if path is None:
            raise ValueError(
                "set_input_files action requires a path.",
            )

        await page.locator(selector).set_input_files(
            path,
            timeout=timeout,
        )

    async def _evaluate(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        value = self._require_value(action)

        await page.evaluate(value)

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

    async def _handle_page_state(
        self,
        context: BrowserInteractionContext[Any],
        page: Page,
    ) -> None:

        inspection = await self._inspector.inspect(
            page,
        )

        if inspection.state not in {
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
            + 120
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
                    "after human intervention."
                )

            await asyncio.sleep(1)