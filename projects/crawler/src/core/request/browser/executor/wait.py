from typing import cast

from core.request.browser.exception import UnsupportedBrowserActionError
from core.request.browser.executor.base import BrowserActionExecutor
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType, LoadState
from playwright.async_api import Page

class WaitActionExecutor(
    BrowserActionExecutor,
):

    _SUPPORTED = frozenset(
        {
            BrowserActionType.WAIT_FOR_URL,
            BrowserActionType.WAIT_FOR_LOAD_STATE,
        },
    )

    def supports(
        self,
        action_type: BrowserActionType,
    ) -> bool:

        return action_type in self._SUPPORTED

    async def execute(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        timeout = self._timeout(action)

        match action.type:

            case BrowserActionType.WAIT_FOR_URL:

                if action.url is None:
                    raise ValueError(
                        "wait_for_url action requires "
                        "a url.",
                    )

                await page.wait_for_url(
                    action.url,
                    timeout=timeout,
                )

            case BrowserActionType.WAIT_FOR_LOAD_STATE:

                if action.state is None:
                    raise ValueError(
                        "wait_for_load_state action requires "
                        "a state:Literal['domcontentloaded', 'load', 'networkidle'].",
                    )
                state=cast(LoadState,action.state)
                await page.wait_for_load_state(
                    state,
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