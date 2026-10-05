from core.request.browser.exception import UnsupportedBrowserActionError
from core.request.browser.executor.base import BrowserActionExecutor
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType
from playwright.async_api import Page


class NavigationActionExecutor(
    BrowserActionExecutor,
):

    _SUPPORTED = frozenset(
        {
            BrowserActionType.GOTO,
            BrowserActionType.GO_BACK,
            BrowserActionType.GO_FORWARD,
            BrowserActionType.RELOAD,
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

        timeout = self._timeout(action)

        match action.type:

            case BrowserActionType.GOTO:

                assert action.url is not None

                await page.goto(
                    action.url,
                    timeout=timeout,
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