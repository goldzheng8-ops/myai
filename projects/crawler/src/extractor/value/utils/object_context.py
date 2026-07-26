from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


@dataclass(slots=True)
class ObjectContext:
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

    _values: dict[str, Any] = field(default_factory=dict)

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

    def update(
        self,
        values: dict[str, Any],
    ) -> None:
        self._values.update(values)

    def remove(self, name: str) -> None:
        self._values.pop(name, None)

    def clear(self) -> None:
        self._values.clear()

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

        if isinstance(value, dict):
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
        """创建子作用域"""

    def pop(self) -> None:
        """退出子作用域"""

    # def copy(self) -> ObjectContext:
    #     """复制上下文"""

    def merge(
        self,
        other: ObjectContext,
    ) -> None:
        """合并上下文"""

    def freeze(self) -> None:
        """只读"""

    def is_frozen(self) -> bool:
        ...