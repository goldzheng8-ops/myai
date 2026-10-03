from abc import ABC, abstractmethod
from typing import Any
from playwright.async_api import Page

from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType
from core.runtime.context import RuntimeContext
from core.runtime.parser import ResolveExpressionParser


class BrowserActionExecutor(ABC):

    def __init__(
        self,
        parser: ResolveExpressionParser,
    ) -> None:
        self._parser = parser

    @abstractmethod
    def supports(
        self,
        action_type: BrowserActionType,
    ) -> bool:
        raise NotImplementedError

    async def execute(
        self,
        page: Page,
        action: BrowserAction,
        context: RuntimeContext,
    ) -> None:
        resolved_action = self._resolve_action(
            action,
            context,
        )

        await self._execute(
            page,
            resolved_action,
        )

    @abstractmethod
    async def _execute(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:
        raise NotImplementedError

    def _resolve_action(
        self,
        action: BrowserAction,
        context: RuntimeContext,
    ) -> BrowserAction:
        updates: dict[str, Any] = {}

        for field_name in self._resolvable_fields():
            value = getattr(
                action,
                field_name,
            )

            resolved = self._resolve_value(
                value,
                context,
            )

            if resolved is not value:
                updates[field_name] = resolved

        if not updates:
            return action

        return action.model_copy(
            update=updates,
        )

    def _resolve_value(
        self,
        value: Any,
        context: RuntimeContext,
    ) -> Any:
        if isinstance(value, str):
            return self._resolve_string(
                value,
                context,
            )

        if isinstance(value, tuple):
            return tuple(
                self._resolve_value(
                    item,
                    context,
                )
                for item in value
            )

        return value

    def _resolve_string(
        self,
        value: str,
        context: RuntimeContext,
    ) -> Any:
        expression = self._parser.parse(
            value,
        )

        if expression is None:
            return value

        return context.resolve_engine.resolve(
            context,
            expression,
        )

    def _resolvable_fields(
        self,
    ) -> tuple[str, ...]:
        return (
            "selector",
            "value",
            "state",
            "url",
            "path",
            "values",
        )