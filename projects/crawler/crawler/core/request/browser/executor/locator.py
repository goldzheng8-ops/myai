from core.request.browser.exception import UnsupportedBrowserActionError
from core.request.browser.executor.base import BrowserActionExecutor
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType
from playwright.async_api import Page

class LocatorActionExecutor(
    BrowserActionExecutor,
):

    _SUPPORTED = frozenset(
        {
            BrowserActionType.CLICK,
            BrowserActionType.DOUBLE_CLICK,
            BrowserActionType.HOVER,
            BrowserActionType.FOCUS,
            BrowserActionType.BLUR,
        },
    )

    def supports(
        self,
        action_type: BrowserActionType,
    ) -> bool:

        return action_type in self._SUPPORTED

    async def _execute(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        if action.selector is None:
            raise ValueError(
                f"{action.type.value!r} action requires "
                "a selector.",
            )

        locator = page.locator(
            action.selector,
        )

        timeout = self._timeout(action)

        match action.type:

            case BrowserActionType.CLICK:

                await locator.click(
                    timeout=timeout,
                    force=action.force,
                    no_wait_after=action.no_wait_after,
                )

            case BrowserActionType.DOUBLE_CLICK:

                await locator.dblclick(
                    timeout=timeout,
                    force=action.force,
                    no_wait_after=action.no_wait_after,
                )

            case BrowserActionType.HOVER:

                await locator.hover(
                    timeout=timeout,
                    force=action.force,
                )

            case BrowserActionType.FOCUS:

                await locator.focus(
                    timeout=timeout,
                )

            case BrowserActionType.BLUR:

                await locator.blur(
                    timeout=timeout,
                )

            case _:

                raise UnsupportedBrowserActionError(
                    action.type,
                )

    @staticmethod
    def _timeout(
        action: BrowserAction,
    ) -> float | None:

        if action.timeout is None:
            return None

        return action.timeout * 1000