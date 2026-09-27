from core.request.browser.exception import UnsupportedBrowserActionError
from core.request.browser.executor.base import BrowserActionExecutor
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType
from playwright.async_api import Page

class KeyboardActionExecutor(
    BrowserActionExecutor,
):

    _SUPPORTED = frozenset(
        {
            BrowserActionType.KEYBOARD_PRESS,
            BrowserActionType.KEYBOARD_TYPE,
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

        if action.value is None:
            raise ValueError(
                f"{action.type.value!r} action requires "
                "a value.",
            )

        match action.type:

            case BrowserActionType.KEYBOARD_PRESS:

                await page.keyboard.press(
                    action.value,
                )

            case BrowserActionType.KEYBOARD_TYPE:

                await page.keyboard.type(
                    action.value,
                )

            case _:

                raise UnsupportedBrowserActionError(
                    action.type,
                )