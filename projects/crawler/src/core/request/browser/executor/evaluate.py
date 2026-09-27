from core.request.browser.executor.base import BrowserActionExecutor
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType
from playwright.async_api import Page

class EvaluateActionExecutor(
    BrowserActionExecutor,
):

    def supports(
        self,
        action_type: BrowserActionType,
    ) -> bool:

        return action_type is BrowserActionType.EVALUATE

    async def execute(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        if action.value is None:
            raise ValueError(
                "evaluate action requires a value.",
            )

        await page.evaluate(
            action.value,
        )