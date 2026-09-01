from collections.abc import Iterable as AbcIterable
from typing import Any, Iterable, List, Optional, cast

from core.template.extension.filter import FilterExtension


def _as_list(value: Any) -> Optional[List[Any]]:
    if value is None or isinstance(value, (str, bytes)):
        return None
    if isinstance(value, AbcIterable):
        return list(cast(Iterable[Any], value))
    return None


class FirstFilter(FilterExtension):
    name = "first"

    def filter(self, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, (list, tuple, str)):
            return value[0] if value else None
        items = _as_list(value)
        if items:
            return items[0]
        return value


class LastFilter(FilterExtension):
    name = "last"

    def filter(self, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, (list, tuple, str)):
            return value[-1] if value else None
        items = _as_list(value)
        if items:
            return items[-1]
        return value


class JoinFilter(FilterExtension):
    name = "join"

    def filter(self, value: Any, sep: str = ",") -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            return value
        items = _as_list(value)
        if items is not None:
            return sep.join(str(item) for item in items)
        return str(value)


class UniqueFilter(FilterExtension):
    name = "unique"

    def filter(self, value: Any) -> Any:
        items = _as_list(value)
        if items is None:
            return value
        seen: set[str] = set()
        result: list[Any] = []
        for item in items:
            key = repr(item)
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result


class SortFilter(FilterExtension):
    name = "sort"

    def filter(self, value: Any, reverse: bool = False) -> Any:
        items = _as_list(value)
        if items is None:
            return value
        return sorted(items, reverse=reverse)


class ReverseFilter(FilterExtension):
    name = "reverse"

    def filter(self, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            return value[::-1]
        items = _as_list(value)
        if items is not None:
            return list(reversed(items))
        return value


class SliceFilter(FilterExtension):
    name = "slice"

    def filter(self, value: Any, start: int = 0, end: int | None = None, step: int = 1) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            return value[start:end:step]
        items = _as_list(value)
        if items is not None:
            return items[start:end:step]
        return value


class FlattenFilter(FilterExtension):
    name = "flatten"

    def filter(self, value: Any) -> Any:
        items = _as_list(value)
        if items is None:
            return value

        result: list[Any] = []
        for item in items:
            nested = _as_list(item)
            if nested is not None:
                result.extend(nested)
            else:
                result.append(item)
        return result


class CompactFilter(FilterExtension):
    name = "compact"

    def filter(self, value: Any) -> Any:
        items = _as_list(value)
        if items is None:
            return value
        return [item for item in items if item not in (None, "", 0, False)]
