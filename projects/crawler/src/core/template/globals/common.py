from typing import Any

from core.template.extension.global_ import GlobalExtension


class LenGlobal(GlobalExtension):
    name = "len"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any) -> int:
        return len(value)


class EnumerateGlobal(GlobalExtension):
    name = "enumerate"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any):
        if args:
            return enumerate(value, *args)
        return enumerate(value)


class ZipGlobal(GlobalExtension):
    name = "zip"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any):
        if value is None:
            return zip()
        if args:
            return zip(value, *args)
        return zip(value)


class RangeGlobal(GlobalExtension):
    name = "range"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any):
        if value is None:
            return range(0)
        return range(value, *args)


class DictGlobal(GlobalExtension):
    name = "dict"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any):
        if value is None:
            return dict()
        if args or kwargs:
            return dict(value, *args, **kwargs)
        return dict(value)


class ListGlobal(GlobalExtension):
    name = "list"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any):
        if value is None:
            return []
        if args or kwargs:
            return list(value, *args, **kwargs)
        return list(value)


class SetGlobal(GlobalExtension):
    name = "set"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any):
        if value is None:
            return set()
        if args or kwargs:
            return set(value, *args, **kwargs)
        return set(value)


class TupleGlobal(GlobalExtension):
    name = "tuple"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any):
        if value is None:
            return ()
        if args or kwargs:
            return tuple(value, *args, **kwargs)
        return tuple(value)


class SortedGlobal(GlobalExtension):
    name = "sorted"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any):
        if value is None:
            return []
        if args or kwargs:
            return sorted(value, *args, **kwargs)
        return sorted(value)


class ReversedGlobal(GlobalExtension):
    name = "reversed"

    def global_(self, value: Any = None, *args: Any, **kwargs: Any):
        if value is None:
            return reversed([])
        return reversed(value)
