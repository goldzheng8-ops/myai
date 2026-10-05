from collections.abc import Iterable as AbcIterable
from typing import Any, Iterable, List, Optional, cast

from core.template.extension.filter import FilterExtension


def _as_list(value: Any) -> Optional[List[Any]]:
    if value is None or isinstance(value, (str, bytes)):
        return None
    if isinstance(value, AbcIterable):
        return list(cast(Iterable[Any], value))
    return None



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
