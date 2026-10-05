from datetime import date, datetime, timedelta, timezone
from typing import Any

from core.template.extension.global_ import GlobalExtension


class NowGlobal(GlobalExtension):
    name = "now"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any) -> datetime:
        if value is None:
            return datetime.now()
        if isinstance(value, timezone):
            return datetime.now(value)
        return datetime.now(tz=value)


class TodayGlobal(GlobalExtension):
    name = "today"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any) -> date:
        return date.today()


class UtcnowGlobal(GlobalExtension):
    name = "utcnow"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any) -> datetime:
        return datetime.now(timezone.utc)


class TimezoneGlobal(GlobalExtension):
    name = "timezone"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any) -> timezone:
        offset = float(value) if value is not None else 0
        name = kwargs.get("name", "UTC")
        return timezone(timedelta(hours=offset), name)


class TimedeltaGlobal(GlobalExtension):
    name = "timedelta"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any) -> timedelta:
        if value is None:
            return timedelta()
        if args:
            return timedelta(value, *args, **kwargs)
        return timedelta(value, **kwargs)