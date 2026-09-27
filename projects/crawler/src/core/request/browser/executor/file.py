from core.request.browser.executor.base import BrowserActionExecutor
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType
from playwright.async_api import Page

class FileActionExecutor(
    BrowserActionExecutor,
):

    def supports(
        self,
        action_type: BrowserActionType,
    ) -> bool:

        return (
            action_type
            is BrowserActionType.SET_INPUT_FILES
        )

    async def execute(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:

        if action.selector is None:
            raise ValueError(
                "set_input_files action requires "
                "a selector.",
            )

        if action.path is None:
            raise ValueError(
                "set_input_files action requires "
                "a path.",
            )

        await page.locator(
            action.selector,
        ).set_input_files(
            action.path,
        )