from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


@dataclass(slots=True)
class RuntimeContext:
    """
    Unified Object Access Layer.

    Stores runtime objects and provides path-based lookup.

    Examples
    --------
    request.url
    response.status
    article.author.name
    items.0.title
    """

    _values: dict[str, Any] = field(
        default_factory=dict,
    )

    _scopes: list[dict[str, Any]] = field(
        default_factory=list,
    )

    _cache: dict[str, Any] = field(
        default_factory=dict,
    )

    _frozen: bool = False

    # ------------------------
    # basic operations
    # ------------------------

    def contains(self, name: str) -> bool:
        return name in self._values

    def get(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        return self._values.get(name, default)

    def set(
        self,
        name: str,
        value: Any,
    ) -> None:
        self._values[name] = value
        self._cache.clear()

    def update(
        self,
        values: dict[str, Any],
    ) -> None:
        self._values.update(values)
        self._cache.clear()

    def remove(self, name: str) -> None:
        self._values.pop(name, None)
        self._cache.clear()

    def clear(self) -> None:
        self._values.clear()
        self._cache.clear()

    def keys(self):
        return self._values.keys()

    def values(self):
        return self._values.values()

    def items(self):
        return self._values.items()

    # ------------------------
    # object resolver
    # ------------------------

    def resolve(
        self,
        path: str,
        default: Any = None,
    ) -> Any:
        """
        Resolve object by dotted path.

        request.url

        response.status

        items.0.title
        """
        cached = self._cache.get(path)

        if cached is not None:
            return cached
        if not path:
            return default

        parts = path.split(".")

        current = self._values.get(parts[0], default)

        if current is default:
            return default

        try:

            for part in parts[1:]:
                current = self._resolve_one(
                    current,
                    part,
                )
            self._cache[path] = current
            return current

        except (
            AttributeError,
            IndexError,
            KeyError,
            TypeError,
            ValueError,
        ):
            return default

    def resolve_many(
        self,
        paths: Iterable[str],
    ) -> dict[str, Any]:

        return {
            path: self.resolve(path)
            for path in paths
        }

    # ------------------------
    # internals
    # ------------------------

    def _resolve_one(
        self,
        value: Any,
        part: str,
    ) -> Any:

        if isinstance(value, Mapping):

            return value[part]

        if isinstance(value, (list, tuple)):

            return value[int(part)]

        return getattr(value, part)

    def as_mapping(self) -> Mapping[str, Any]:
        """
        Expose the top-level context as a read-only mapping.
        """

        return self._values

    def push(self) -> None:

        self._scopes.append(
            self._values,
        )

        self._values = self._values.copy()

        self._cache.clear()

    def pop(self) -> None:

        if not self._scopes:
            raise RuntimeError(
                "Scope stack is empty."
            )

        self._values = self._scopes.pop()

        self._cache.clear()
    def merge(
        self,
        other: RuntimeContext,
    ) -> None:

        self._values.update(
            other._values,
        )

        self._cache.clear()

    def freeze(self) -> None:
        self._frozen = True

    def is_frozen(self) -> bool:
        return self._frozen