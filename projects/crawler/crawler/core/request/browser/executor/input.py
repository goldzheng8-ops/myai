from core.request.browser.exception import UnsupportedBrowserActionError
from core.request.browser.executor.base import BrowserActionExecutor
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType
from playwright.async_api import Page

class InputActionExecutor(
    BrowserActionExecutor,
):

    _SUPPORTED = frozenset(
        {
            BrowserActionType.FILL,
            BrowserActionType.TYPE,
            BrowserActionType.CLEAR,
            BrowserActionType.PRESS,
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

            case BrowserActionType.FILL:

                assert action.value is not None

                await locator.fill(
                    action.value,
                    timeout=timeout,
                    force=action.force,
                    no_wait_after=action.no_wait_after,
                )

            case BrowserActionType.TYPE:

                assert action.value is not None

                await locator.press_sequentially(
                    action.value,
                    timeout=timeout,
                )

            case BrowserActionType.CLEAR:

                await locator.clear(
                    timeout=timeout,
                    force=action.force,
                )

            case BrowserActionType.PRESS:

                assert action.value is not None

                await locator.press(
                    action.value,
                    timeout=timeout,
                    no_wait_after=action.no_wait_after,
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