from core.request.browser.inspector.model import BrowserPageInspection
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

class HumanInterventionError(
    RuntimeError,
):
    pass

class HumanInterventionTimeoutError(
    HumanInterventionError,
):

    def __init__(
        self,
        *,
        inspection: BrowserPageInspection,
    ) -> None:

        self.inspection = inspection

        super().__init__(
            "Human intervention timed out: "
            f"state={inspection.state.value!r}, "
            f"url={inspection.url!r}",
        )

class BrowserPageRecoveryError(
    RuntimeError,
):
    pass

class BrowserPageRecoveryTimeoutError(
    BrowserPageRecoveryError,
):

    def __init__(
        self,
        *,
        inspection: BrowserPageInspection,
    ) -> None:

        self.inspection = inspection

        super().__init__(
            "Browser page did not recover "
            "after human intervention: "
            f"state={inspection.state.value!r}, "
            f"url={inspection.url!r}",
        )