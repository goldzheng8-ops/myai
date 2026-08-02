import math
from typing import Any

from core.template.extension.filter import FilterExtension


def _coerce_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.replace(",", "").replace("_", "").strip()
        if not text:
            return None
        try:
            return float(text)
        except ValueError:
            return None
    return None


class RoundFilter(FilterExtension):
    name = "round"

    def filter(self, value: Any, digits: int = 0) -> Any:
        num = _coerce_number(value)
        if num is None:
            return value
        return round(num, digits)


class CeilFilter(FilterExtension):
    name = "ceil"

    def filter(self, value: Any) -> Any:
        num = _coerce_number(value)
        if num is None:
            return value
        return math.ceil(num)


class FloorFilter(FilterExtension):
    name = "floor"

    def filter(self, value: Any) -> Any:
        num = _coerce_number(value)
        if num is None:
            return value
        return math.floor(num)


class AbsFilter(FilterExtension):
    name = "abs"

    def filter(self, value: Any) -> Any:
        num = _coerce_number(value)
        if num is None:
            return value
        return abs(num)


class ClampFilter(FilterExtension):
    name = "clamp"

    def filter(self, value: Any, minimum: float = 0, maximum: float = 100) -> Any:
        num = _coerce_number(value)
        if num is None:
            return value
        return max(minimum, min(num, maximum))


class PercentFilter(FilterExtension):
    name = "percent"

    def filter(self, value: Any, total: float | None = None, digits: int = 2) -> Any:
        num = _coerce_number(value)
        if num is None:
            return value
        if total is None:
            result = num * 100
        else:
            total_num = _coerce_number(total)
            if total_num in (None, 0):
                return value
            result = (num / total_num) * 100
        return round(result, digits)


class CurrencyFilter(FilterExtension):
    name = "currency"

    def filter(self, value: Any, symbol: str = "$", digits: int = 2) -> Any:
        num = _coerce_number(value)
        if num is None:
            return value
        return f"{symbol}{num:,.{digits}f}"


class ThousandsFilter(FilterExtension):
    name = "thousands"

    def filter(self, value: Any, digits: int = 0) -> Any:
        num = _coerce_number(value)
        if num is None:
            return value
        return f"{num:,.{digits}f}"


class ScientificFilter(FilterExtension):
    name = "scientific"

    def filter(self, value: Any, digits: int = 3) -> Any:
        num = _coerce_number(value)
        if num is None:
            return value
        return f"{num:.{digits}e}"


class FilesizeFilter(FilterExtension):
    name = "filesize"

    def filter(self, value: Any, binary: bool = True) -> Any:
        num = _coerce_number(value)
        if num is None:
            return value
        units = ["B", "KB", "MB", "GB", "TB", "PB"] if binary else ["B", "kB", "MB", "GB", "TB", "PB"]
        size = float(num)
        base = 1024 if binary else 1000
        for unit in units:
            if size < base or unit == units[-1]:
                if unit == "B":
                    return f"{int(size)} {unit}"
                return f"{size / (base ** (units.index(unit))):.2f} {unit}"
            size /= base
        return f"{size:.2f} {units[-1]}"
