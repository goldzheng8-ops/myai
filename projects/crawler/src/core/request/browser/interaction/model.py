from __future__ import annotations
from pydantic import model_validator


from core.request.browser.typing import BrowserActionType
from core.typing.config import BaseConfig


_SELECTOR_ACTIONS = frozenset(
    {
        BrowserActionType.FILL,
        BrowserActionType.TYPE,
        BrowserActionType.CLEAR,
        BrowserActionType.PRESS,
        BrowserActionType.CLICK,
        BrowserActionType.DOUBLE_CLICK,
        BrowserActionType.HOVER,
        BrowserActionType.FOCUS,
        BrowserActionType.BLUR,
        BrowserActionType.SELECT,
        BrowserActionType.CHECK,
        BrowserActionType.UNCHECK,
        BrowserActionType.SET_INPUT_FILES,
    }
)

_VALUE_ACTIONS = frozenset(
    {
        BrowserActionType.FILL,
        BrowserActionType.TYPE,
        BrowserActionType.PRESS,
        BrowserActionType.SELECT,
        BrowserActionType.KEYBOARD_PRESS,
        BrowserActionType.KEYBOARD_TYPE,
        BrowserActionType.WAIT_FOR_URL,
        BrowserActionType.WAIT_FOR_LOAD_STATE,
        BrowserActionType.EVALUATE,
    }
)

class BrowserAction(BaseConfig):

    type: BrowserActionType

    selector: str | None = None

    value: str | None = None

    timeout: float | None = None

    state: str | None = None

    url: str | None = None

    path: str | None = None

    values: tuple[str, ...] = ()

    force: bool = False

    no_wait_after: bool = False

    strict: bool = False

    @model_validator(mode="after")
    def validate_action(self) -> BrowserAction:

        if self.type in _SELECTOR_ACTIONS:
            if self.selector is None:
                raise ValueError(
                    f"{self.type.value!r} action requires "
                    "a selector.",
                )

        if self.type in _VALUE_ACTIONS:
            if self.value is None:
                raise ValueError(
                    f"{self.type.value!r} action requires "
                    "a value.",
                )

        if self.type == BrowserActionType.SET_INPUT_FILES:
            if self.path is None:
                raise ValueError(
                    "set_input_files action requires "
                    "a path.",
                )

        if self.type == BrowserActionType.GOTO:
            if self.url is None:
                raise ValueError(
                    "goto action requires a url.",
                )

        return self
