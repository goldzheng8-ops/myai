from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from core.template.extension.test import TestExtension


class NoneTest(TestExtension):
    name = "none"

    def test(self, value: Any) -> bool:
        return value is None


class EmptyTest(TestExtension):
    name = "empty"

    def test(self, value: Any) -> bool:
        if value is None:
            return True
        if isinstance(value, (str, list, tuple, set, dict)):
            return len(value) == 0
        return False


class BlankTest(TestExtension):
    name = "blank"

    def test(self, value: Any) -> bool:
        if value is None:
            return True
        if isinstance(value, str):
            return value.strip() == ""
        return False


class NumberTest(TestExtension):
    name = "number"

    def test(self, value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool)


class StringTest(TestExtension):
    name = "string"

    def test(self, value: Any) -> bool:
        return isinstance(value, str)


class MappingTest(TestExtension):
    name = "mapping"

    def test(self, value: Any) -> bool:
        return isinstance(value, Mapping)


class SequenceTest(TestExtension):
    name = "sequence"

    def test(self, value: Any) -> bool:
        return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


class CallableTest(TestExtension):
    name = "callable"

    def test(self, value: Any) -> bool:
        return callable(value)


class IterableTest(TestExtension):
    name = "iterable"

    def test(self, value: Any) -> bool:
        return isinstance(value, Iterable) and not isinstance(value, (str, bytes, bytearray))


class TruthyTest(TestExtension):
    name = "truthy"

    def test(self, value: Any) -> bool:
        return bool(value)


class FalsyTest(TestExtension):
    name = "falsy"

    def test(self, value: Any) -> bool:
        return not bool(value)
