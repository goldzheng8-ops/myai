from core.request.browser.executor.base import BrowserActionExecutor
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType
from playwright.async_api import Page

class SelectionActionExecutor(
    BrowserActionExecutor,
):

    def supports(
        self,
        action_type: BrowserActionType,
    ) -> bool:

        return action_type is BrowserActionType.SELECT

    async def execute(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        if action.selector is None:
            raise ValueError(
                "select action requires a selector.",
            )

        locator = page.locator(
            action.selector,
        )

        values = action.values

        if not values:

            if action.value is None:
                raise ValueError(
                    "select action requires value "
                    "or values.",
                )

            values = (action.value,)

        await locator.select_option(
            list(values),
            timeout=self._timeout(action),
        )

    @staticmethod
    def _timeout(
        action: BrowserAction,
    ) -> float | None:

        if action.timeout is None:
            return None

        return action.timeout * 1000