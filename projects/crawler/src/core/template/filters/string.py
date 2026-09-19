from __future__ import annotations

import hashlib
import re
from pathlib import PurePosixPath
from typing import Any
from urllib.parse import urlparse

from core.template.extension.filter import FilterExtension


def _as_text(value: Any) -> str | None:
    if value is None:
        return None

    if isinstance(value, str):
        return value

    return str(value)


def _split_words(value: str) -> list[str]:
    words = re.split(r"[_\s\-]+", value.strip())
    return [word for word in words if word]


class StripFilter(FilterExtension):
    name = "strip"

    def filter(self, value: Any) -> Any:
        text = _as_text(value)
        return text.strip() if text is not None else value


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


class BasenameFilter(FilterExtension):
    name = "basename"

    def filter(
        self,
        value: Any,
    ) -> Any:

        text = _as_text(value)

        if text is None:
            return value

        return PurePosixPath(text).name


class ExtensionFilter(FilterExtension):
    name = "extension"

    def filter(
        self,
        value: Any,
    ) -> Any:

        text = _as_text(value)

        if text is None:
            return value

        parsed = urlparse(text)

        path = parsed.path

        if not path:
            return ""

        suffix = PurePosixPath(path).suffix

        if not suffix:
            return ""

        return suffix.lstrip(".").lower()


class Sha256Filter(FilterExtension):
    name = "sha256"

    def filter(
        self,
        value: Any,
    ) -> Any:

        if value is None:
            return value

        if isinstance(value, bytes):
            data = value
        elif isinstance(value, bytearray):
            data = bytes(value)
        else:
            data = str(value).encode("utf-8")

        return hashlib.sha256(data).hexdigest()


class SlugifyFilter(FilterExtension):
    name = "slugify"

    def filter(
        self,
        value: Any,
    ) -> Any:

        text = _as_text(value)

        if text is None:
            return value

        text = text.strip().lower()

        text = re.sub(
            r"[^a-zA-Z0-9]+",
            "-",
            text,
        )

        return text.strip("-")


class SafeFilenameFilter(FilterExtension):
    name = "safe_filename"

    def filter(
        self,
        value: Any,
    ) -> Any:

        text = _as_text(value)

        if text is None:
            return value

        text = text.strip()

        # Windows + Linux/macOS 中都不适合作为文件名的字符
        text = re.sub(
            r'[<>:"/\\|?*\x00-\x1f]',
            "_",
            text,
        )

        # Windows 文件名不能以空格或句号结尾
        text = text.rstrip(" .")

        # 避免 Windows 保留设备名
        if text.upper() in {
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        }:
            text = f"_{text}"

        return text

class StemFilter(FilterExtension):
    name = "stem"

    def filter(
        self,
        value: Any,
    ) -> Any:

        text = _as_text(value)

        if text is None:
            return value

        return PurePosixPath(text).stem