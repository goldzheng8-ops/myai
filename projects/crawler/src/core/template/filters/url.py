"""URL-related template filters.

Provided filters:
- `urlencode`: convert mapping/sequence to query string
- `urldecode`: parse query string into a dict
- `quote`: percent-encode a string
- `unquote`: percent-decode a string
- `join_url`: join a base URL with path segments
- `query`: extract query params from a URL or query string
"""

from typing import Any, Dict, List, Optional, cast
from urllib.parse import (
	parse_qs,
	quote as _quote,
	unquote as _unquote,
	urlencode as _urlencode,
	urljoin,
	urlparse,
)

from core.template.extension.filter import FilterExtension


from collections.abc import Sequence



class UrlEncodeFilter(FilterExtension):

    name = "urlencode"

    def filter(
        self,
        value: Any,
    ) -> str:

        if value is None:
            return ""

        if isinstance(value, dict):

            raw = cast(
                dict[Any, Any],
                value,
            )

            query = {
                str(key): item
                for key, item in raw.items()
            }

            return _urlencode(
                query,
                doseq=True,
            )

        if isinstance(value, (list, tuple)):

            sequence = cast(
                Sequence[Any],
                value,
            )

            return _urlencode(
                sequence,
                doseq=True,
            )

        return str(value)


class UrlDecodeFilter(FilterExtension):
	name = "urldecode"

	def filter(self, value: Any) -> Dict[str, List[str]]:
		if value is None:
			return {}
		if isinstance(value, dict):
			return value  # type: ignore[return-value]
		text = str(value)
		# parse_qs returns dict[str, list[str]]
		return parse_qs(text, keep_blank_values=True)


class QuoteFilter(FilterExtension):
	name = "quote"

	def filter(self, value: Any, safe: str = "/") -> str:
		if value is None:
			return ""
		return _quote(str(value), safe=safe)


class UnquoteFilter(FilterExtension):
	name = "unquote"

	def filter(self, value: Any) -> str:
		if value is None:
			return ""
		return _unquote(str(value))


class JoinUrlFilter(FilterExtension):
	name = "join_url"

	def filter(self, value: Any, *parts: Any) -> str:
		if value is None:
			return ""
		base = str(value)
		result = base
		for p in parts:
			result = urljoin(result.rstrip("/") + "/", str(p))
		return result


class QueryFilter(FilterExtension):
	"""Extract query params.

	Usage:
	  - `query(url_or_qs)` -> dict[str, list[str]]
	  - `query(url_or_qs, name)` -> first value or None
	"""

	name = "query"

	def filter(self, value: Any, name: Optional[str] = None) -> Any:
		if value is None:
			return {} if name is None else None
		text = str(value)
		# If looks like a full URL, extract the query part
		parsed = urlparse(text)
		qs = parsed.query if parsed.query else text
		params = parse_qs(qs, keep_blank_values=True)
		if name is None:
			return params
		vals = params.get(name)
		return vals[0] if vals else None
