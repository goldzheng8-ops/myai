from abc import ABC, abstractmethod
from typing import Any, Generic, Sequence

from core.runtime.context import RuntimeContext
from core.runtime.errors import InvalidExpressionError, PathNotFoundError
from core.runtime.expression import DotPathExpression
from core.runtime.options import DotPathOptions
from core.runtime.protocol import AccessorProvider
from core.runtime.typing import ExpressionT


class ResolveStrategy(
    Generic[ExpressionT],
    ABC,
):

    @abstractmethod
    def resolve(
        self,
        context: RuntimeContext,
        expression: ExpressionT,
    ) -> Any:
        ...

class DotPathStrategy(
    ResolveStrategy[
        DotPathExpression
    ]
):

    expression_type = DotPathExpression

    def __init__(
        self,
        provider: AccessorProvider,
        *,
        options: DotPathOptions | None = None,
    ):

        self._provider = provider

        self._options = (
            options
            or DotPathOptions()
        )
    def resolve(
        self,
        context: RuntimeContext,
        expression: DotPathExpression,
    ) -> Any:

        cache = context.cache

        if (
            not self._options.cache_enabled
            or cache is None
        ):
            return self._resolve(
                context,
                expression,
            )

        return cache.put_if_absent(
            expression.cache_key,
            lambda: self._resolve(
                context,
                expression,
            ),
        )

    def _resolve(
        self,
        context: RuntimeContext,
        expression: DotPathExpression,
    ) -> Any:

        parts = self._split(expression.path)

        root = self._resolve_root(
            context,
            parts[0],
        )

        return self._walk(
            root,
            parts[1:],
        )

    def _walk(
        self,
        value: Any,
        parts: Sequence[str],
    ) -> Any:

        current = value

        for part in parts:

            current = self._access(
                current,
                part,
            )

        return current

    def _access(
        self,
        value: Any,
        key: str,
    ) -> Any:

        for accessor in self._provider.accessors():

            if not accessor.supports(value):
                continue

            try:

                return accessor.access(
                    value,
                    key,
                )

            except (
                AttributeError,
                LookupError,
                KeyError,
                IndexError,
                TypeError,
                ValueError,
            ):
                break

        if self._options.ignore_missing:
            return None

        raise PathNotFoundError(key)

    def _resolve_root(
        self,
        context: RuntimeContext,
        name: str,
    ) -> Any:

        sentinel = object()

        value = context.get(
            name,
            sentinel,
        )

        if value is sentinel:

            raise PathNotFoundError(
                f"Variable '{name}' not found."
            )

        return value

    def _split(
        self,
        path: str,
    ) -> tuple[str,...]:

        if not path.strip():

            raise InvalidExpressionError(
                "Empty expression."
            )

        return tuple(
            part
            for part in path.split(
                self._options.separator
            )
            if part
        )
