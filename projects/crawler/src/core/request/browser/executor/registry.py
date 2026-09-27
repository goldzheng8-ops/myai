from core.registry import Registry
from core.request.browser.exception import UnsupportedBrowserActionError
from core.request.browser.executor.base import BrowserActionExecutor
from core.request.browser.typing import BrowserActionType


class BrowserActionExecutorRegistry(
    Registry[
        str,
        BrowserActionExecutor,
    ],
):

    def resolve(
        self,
        action_type: BrowserActionType,
    ) -> BrowserActionExecutor:

        for executor in self.values():

            if executor.supports(action_type):
                return executor

        raise UnsupportedBrowserActionError(
            action_type,
        )