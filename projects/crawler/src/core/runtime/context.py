from __future__ import annotations
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Self

from core.cache.protocol import Cache
from core.runtime.engine import ResolveEngine
from core.runtime.expression import DotPathExpression, ResolveExpression

from .scope import RuntimeScope


@dataclass(slots=True)
class RuntimeContext:

    _scopes: list[RuntimeScope] = field(
        default_factory=lambda: [
            RuntimeScope(name="global")
        ]
    )

    _cache: Cache[str, Any] | None = None

    _resolver: ResolveEngine | None = None

    _frozen: bool = False

    @property
    def resolver(
        self,
    ) -> ResolveEngine | None:

        return self._resolver

    def set_resolver(
        self,
        resolver: ResolveEngine | None,
    ) -> None:
        """
        Configure the resolve engine.
        """

        self._ensure_mutable()

        self._resolver = resolver

    def resolve(
        self,
        expression: ResolveExpression,
    ) -> Any:
        if isinstance(
            expression,
            str,
        ):
            expression = DotPathExpression(
                expression
            )

        if self._resolver is None:

            raise RuntimeError(
                "ResolveEngine not configured."
            )

        return self._resolver.resolve(
            self,
            expression,
        )

    @property
    def cache(self) -> Cache[str, Any] | None:
        return self._cache
    @property
    def current_scope(self) -> RuntimeScope:
        return self._scopes[-1]

    @property
    def scopes(self) -> tuple[RuntimeScope, ...]:
        return tuple(self._scopes)

    def _clear_cache(self) -> None:
        if self._cache is not None:
            self._cache.clear()

    def _ensure_mutable(self) -> None:
        if self._frozen:
            raise RuntimeError(
                "RuntimeContext is frozen."
            )

    def contains(
        self,
        name: str,
    ) -> bool:

        return any(
            scope.contains(name)
            for scope in reversed(self._scopes)
        )

    def get(
        self,
        name: str,
        default: Any = None,
    ) -> Any:

        for scope in reversed(self._scopes):

            if scope.contains(name):
                return scope.get(name)

        return default

    def keys(self):

        return self.flatten().keys()

    def values(self):

        return self.flatten().values()

    def items(self):

        return self.flatten().items()

    def set(
        self,
        name: str,
        value: Any,
    ) -> None:

        self._ensure_mutable()

        self.current_scope.set(
            name,
            value,
        )

        self._clear_cache()

    def update(
        self,
        values: Mapping[str, Any],
    ) -> None:

        self._ensure_mutable()

        self.current_scope.values.update(values)

        self._clear_cache()

    def remove(
        self,
        name: str,
    ) -> None:

        self._ensure_mutable()

        self.current_scope.remove(name)

        self._clear_cache()

    def clear(self) -> None:

        self._ensure_mutable()

        self.current_scope.clear()

        self._clear_cache()

    def push(
        self,
        *,
        name: str = "",
    ) -> RuntimeScope:

        self._ensure_mutable()

        scope = RuntimeScope(
            name=name,
        )

        self._scopes.append(scope)

        self._clear_cache()

        return scope

    def pop(
        self,
    ) -> RuntimeScope:

        self._ensure_mutable()

        if len(self._scopes) == 1:
            raise RuntimeError(
                "Cannot pop global scope."
            )

        scope = self._scopes.pop()

        self._clear_cache()

        return scope

    def merge(
        self,
        other: RuntimeContext,
    ) -> None:

        self._ensure_mutable()

        self.current_scope.values.update(
            other.current_scope.values,
        )

        self._clear_cache()

    def flatten(
        self,
    ) -> dict[str, Any]:

        merged: dict[str, Any] = {}

        for scope in self._scopes:
            merged.update(
                scope.values
            )

        return merged

    def copy(
        self,
    ) -> Self:

        return type(self)(
            _scopes=[
                RuntimeScope(
                    name=scope.name,
                    readonly=scope.readonly,
                    values=dict(scope.values),
                )
                for scope in self._scopes
            ],
            _cache=None,
            _resolver=self._resolver,
            _frozen=self._frozen,
        )

    def as_mapping(
        self,
    ) -> Mapping[str, Any]:

        return MappingProxyType(
            self.flatten()
        )

    def freeze(self) -> None:

        self._frozen = True

    def unfreeze(self) -> None:

        self._frozen = False

    @property
    def frozen(self) -> bool:

        return self._frozen