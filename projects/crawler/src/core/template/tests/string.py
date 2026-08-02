import re
from typing import Any

from core.template.extension.test import TestExtension


class StartswithTest(TestExtension):
    name = "startswith"

    def test(self, value: Any, prefix: str = "") -> bool:
        return isinstance(value, str) and value.startswith(prefix)


class EndswithTest(TestExtension):
    name = "endswith"

    def test(self, value: Any, suffix: str = "") -> bool:
        return isinstance(value, str) and value.endswith(suffix)


class ContainsTest(TestExtension):
    name = "contains"

    def test(self, value: Any, needle: str = "") -> bool:
        return isinstance(value, str) and needle in value


class MatchTest(TestExtension):
    name = "match"

    def test(self, value: Any, pattern: str = "") -> bool:
        return isinstance(value, str) and re.match(pattern, value) is not None


class SearchTest(TestExtension):
    name = "search"

    def test(self, value: Any, pattern: str = "") -> bool:
        return isinstance(value, str) and re.search(pattern, value) is not None


class RegexTest(TestExtension):
    name = "regex"

    def test(self, value: Any, pattern: str = "") -> bool:
        return isinstance(value, str) and re.fullmatch(pattern, value) is not None


class LowerTest(TestExtension):
    name = "lower"

    def test(self, value: Any) -> bool:
        return isinstance(value, str) and value == value.lower()


class UpperTest(TestExtension):
    name = "upper"

    def test(self, value: Any) -> bool:
        return isinstance(value, str) and value == value.upper()


class TitleTest(TestExtension):
    name = "title"

    def test(self, value: Any) -> bool:
        return isinstance(value, str) and value == value.title()


class DigitTest(TestExtension):
    name = "digit"

    def test(self, value: Any) -> bool:
        return isinstance(value, str) and value.isdigit()


class AlphaTest(TestExtension):
    name = "alpha"

    def test(self, value: Any) -> bool:
        return isinstance(value, str) and value.isalpha()


class AlnumTest(TestExtension):
    name = "alnum"

    def test(self, value: Any) -> bool:
        return isinstance(value, str) and value.isalnum()


class AsciiTest(TestExtension):
    name = "ascii"

    def test(self, value: Any) -> bool:
        return isinstance(value, str) and value.isascii()
