import re
from typing import Any

from core.template.extension.filter import FilterExtension


def _as_text(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _split_words(value: str) -> list[str]:
    words = re.split(r"[_\s\-]+", value.strip())
    return [word for word in words if word]


class StripFilter(FilterExtension):
    name = "strip"

    def filter(self, value: Any) -> Any:
        text = _as_text(value)
        return text.strip() if text is not None else value


class LowerFilter(FilterExtension):
    name = "lower"

    def filter(self, value: Any) -> Any:
        text = _as_text(value)
        return text.lower() if text is not None else value


class UpperFilter(FilterExtension):
    name = "upper"

    def filter(self, value: Any) -> Any:
        text = _as_text(value)
        return text.upper() if text is not None else value


class CapitalizeFilter(FilterExtension):
    name = "capitalize"

    def filter(self, value: Any) -> Any:
        text = _as_text(value)
        return text.capitalize() if text is not None else value


class TitleFilter(FilterExtension):
    name = "title"

    def filter(self, value: Any) -> Any:
        text = _as_text(value)
        return text.title() if text is not None else value


class ReplaceFilter(FilterExtension):
    name = "replace"

    def filter(self, value: Any, old: str = "", new: str = "") -> Any:
        text = _as_text(value)
        if text is None:
            return value
        return text.replace(old, new)


class TruncateFilter(FilterExtension):
    name = "truncate"

    def filter(self, value: Any, length: int = 80, suffix: str = "...") -> Any:
        text = _as_text(value)
        if text is None:
            return value
        if len(text) <= length:
            return text
        if length <= len(suffix):
            return suffix[:length]
        return text[: length - len(suffix)] + suffix


class SlugFilter(FilterExtension):
    name = "slug"

    def filter(self, value: Any) -> Any:
        text = _as_text(value)
        if text is None:
            return value
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
        return slug.strip("-")


class SnakeCaseFilter(FilterExtension):
    name = "snake_case"

    def filter(self, value: Any) -> Any:
        text = _as_text(value)
        if text is None:
            return value
        words = _split_words(text)
        if not words:
            return ""
        return "_".join(word.lower() for word in words)


class CamelCaseFilter(FilterExtension):
    name = "camel_case"

    def filter(self, value: Any) -> Any:
        text = _as_text(value)
        if text is None:
            return value
        words = _split_words(text)
        if not words:
            return ""
        return words[0].lower() + "".join(word[:1].upper() + word[1:].lower() for word in words[1:])


class PascalCaseFilter(FilterExtension):
    name = "pascal_case"

    def filter(self, value: Any) -> Any:
        text = _as_text(value)
        if text is None:
            return value
        words = _split_words(text)
        if not words:
            return ""
        return "".join(word[:1].upper() + word[1:].lower() for word in words)


class KebabCaseFilter(FilterExtension):
    name = "kebab_case"

    def filter(self, value: Any) -> Any:
        text = _as_text(value)
        if text is None:
            return value
        words = _split_words(text)
        if not words:
            return ""
        return "-".join(word.lower() for word in words)


class RegexReplaceFilter(FilterExtension):
    name = "regex_replace"

    def filter(self, value: Any, pattern: str = "", replacement: str = "") -> Any:
        text = _as_text(value)
        if text is None:
            return value
        return re.sub(pattern, replacement, text)