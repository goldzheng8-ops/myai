import html as html_lib
import re
from typing import Any
import markdown as markdown_lib

from core.template.extension.filter import FilterExtension



class StripHtmlFilter(FilterExtension):
    name = "strip_html"

    def filter(self, value: Any) -> Any:
        if value is None:
            return value
        return re.sub(r"<[^>]+>", "", str(value))


class EscapeHtmlFilter(FilterExtension):
    name = "escape_html"

    def filter(self, value: Any) -> Any:
        if value is None:
            return value
        return html_lib.escape(str(value), quote=False)


class UnescapeHtmlFilter(FilterExtension):
    name = "unescape_html"

    def filter(self, value: Any) -> Any:
        if value is None:
            return value
        return html_lib.unescape(str(value))


class MarkdownFilter(FilterExtension):
    name = "markdown"

    def filter(self, value: Any) -> Any:
        if value is None:
            return value
        text = str(value)
        if markdown_lib is not None:
            return markdown_lib.markdown(text)
        return text


class PlaintextFilter(FilterExtension):
    name = "plaintext"

    def filter(self, value: Any) -> Any:
        return StripHtmlFilter().filter(value)
