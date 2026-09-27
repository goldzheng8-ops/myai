from core.request.browser.typing import BrowserActionType


class UnsupportedBrowserActionError(
    RuntimeError,
):
    def __init__(
        self,
        action_type: BrowserActionType,
    ) -> None:

        self.action_type = action_type

        super().__init__(
            "No browser action executor supports "
            f"action type {action_type.value!r}.",
        )