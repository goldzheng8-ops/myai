from __future__ import annotations

from datetime import date, datetime, time
from typing import Any

from core.template.extension.filter import FilterExtension


def _to_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, time.min)
    if isinstance(value, str):
        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%d",
        ):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    return None


class DatetimeFilter(FilterExtension):
    name = "datetime"

    def filter(self, value: Any, fmt: str = "%Y-%m-%d %H:%M:%S") -> Any:
        dt = _to_datetime(value)
        if dt is None:
            return value
        return dt.strftime(fmt)


class DateFilter(FilterExtension):
    name = "date"

    def filter(self, value: Any, fmt: str = "%Y-%m-%d") -> Any:
        dt = _to_datetime(value)
        if dt is None:
            return value
        return dt.date().strftime(fmt)


class TimeFilter(FilterExtension):
    name = "time"

    def filter(self, value: Any, fmt: str = "%H:%M:%S") -> Any:
        dt = _to_datetime(value)
        if dt is None:
            return value
        return dt.time().strftime(fmt)


class TimestampFilter(FilterExtension):
    name = "timestamp"

    def filter(self, value: Any) -> Any:
        dt = _to_datetime(value)
        if dt is None:
            return value
        return int(dt.timestamp())


class IsoformatFilter(FilterExtension):
    name = "isoformat"

    def filter(self, value: Any) -> Any:
        dt = _to_datetime(value)
        if dt is None:
            return value
        return dt.isoformat()


class HumanizeFilter(FilterExtension):
    name = "humanize"

    def filter(self, value: Any) -> Any:
        dt = _to_datetime(value)
        if dt is None:
            return value

        delta = datetime.now() - dt
        seconds = max(0, int(delta.total_seconds()))

        if seconds < 60:
            return "just now" if seconds < 10 else f"{seconds} seconds ago"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        hours = minutes // 60
        if hours < 24:
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        days = hours // 24
        return f"{days} day{'s' if days != 1 else ''} ago"
