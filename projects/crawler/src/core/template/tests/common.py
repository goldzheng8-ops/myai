from collections.abc import Sized
from typing import Any

from core.template.extension.test import TestExtension


class EmptyTest(TestExtension):
    name = "empty"

    def test(self, value: Any) -> bool:
        if value is None:
            return True
        if isinstance(value, Sized):
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


class TruthyTest(TestExtension):
    name = "truthy"

    def test(self, value: Any) -> bool:
        return bool(value)


class FalsyTest(TestExtension):
    name = "falsy"

    def test(self, value: Any) -> bool:
        return not bool(value)
