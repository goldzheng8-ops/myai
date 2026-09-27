from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping
from pydantic import model_validator


from core.request.browser.typing import BrowserActionType
from core.typing.config import BaseConfig

@dataclass(frozen=True, slots=True)
class BrowserActionSpec:

    required: frozenset[str] = frozenset()

    allowed: frozenset[str] = frozenset()

_BROWSER_ACTION_SPECS: Mapping[
    BrowserActionType,
    BrowserActionSpec,
] = {
    BrowserActionType.CLICK: BrowserActionSpec(
        required=frozenset({"selector"}),
        allowed=frozenset({
            "selector",
            "timeout",
            "force",
            "no_wait_after",
            "strict",
        }),
    ),

    BrowserActionType.FILL: BrowserActionSpec(
        required=frozenset({
            "selector",
            "value",
        }),
        allowed=frozenset({
            "selector",
            "value",
            "timeout",
            "force",
            "no_wait_after",
            "strict",
        }),
    ),

    BrowserActionType.GOTO: BrowserActionSpec(
        required=frozenset({"url"}),
        allowed=frozenset({
            "url",
            "timeout",
            "no_wait_after",
        }),
    ),

    BrowserActionType.SELECT: BrowserActionSpec(
        required=frozenset({
            "selector",
            "values",
        }),
        allowed=frozenset({
            "selector",
            "values",
            "timeout",
            "force",
            "no_wait_after",
            "strict",
        }),
    ),

    BrowserActionType.SET_INPUT_FILES: BrowserActionSpec(
        required=frozenset({
            "selector",
            "path",
        }),
        allowed=frozenset({
            "selector",
            "path",
            "timeout",
            "no_wait_after",
        }),
    ),

    BrowserActionType.WAIT_FOR_URL: BrowserActionSpec(
        required=frozenset({"value"}),
        allowed=frozenset({
            "value",
            "timeout",
        }),
    ),

    BrowserActionType.WAIT_FOR_LOAD_STATE: BrowserActionSpec(
        required=frozenset({"state"}),
        allowed=frozenset({
            "state",
            "timeout",
        }),
    ),

    BrowserActionType.EVALUATE: BrowserActionSpec(
        required=frozenset({"value"}),
        allowed=frozenset({
            "value",
            "timeout",
        }),
    ),
}
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
    def validate_action(
        self,
    ) -> BrowserAction:

        spec = _BROWSER_ACTION_SPECS.get(
            self.type,
        )

        if spec is None:
            raise ValueError(
                f"Unsupported browser action: "
                f"{self.type.value!r}.",
            )

        provided = self._provided_fields()

        missing = (
            spec.required - provided
        )

        if missing:
            field = next(iter(missing))

            raise ValueError(
                f"{self.type.value!r} action requires "
                f"a {field}.",
            )

        unsupported = (
            provided - spec.allowed
        )

        if unsupported:
            field = next(iter(unsupported))

            raise ValueError(
                f"{self.type.value!r} action does not "
                f"support field {field!r}.",
            )

        return self

    def _provided_fields(
        self,
    ) -> set[str]:

        result: set[str] = set()

        if self.selector is not None:
            result.add("selector")

        if self.value is not None:
            result.add("value")

        if self.timeout is not None:
            result.add("timeout")

        if self.state is not None:
            result.add("state")

        if self.url is not None:
            result.add("url")

        if self.path is not None:
            result.add("path")

        if self.values:
            result.add("values")

        if self.force:
            result.add("force")

        if self.no_wait_after:
            result.add("no_wait_after")

        if self.strict:
            result.add("strict")

        return result