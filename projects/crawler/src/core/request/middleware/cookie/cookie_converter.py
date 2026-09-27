from datetime import datetime, timezone
from http.cookiejar import Cookie as StdlibCookie
from typing import Iterable
from urllib.parse import urlparse

from core.request.middleware.cookie.model import Cookie, SameSite
from core.request.middleware.cookie.policy.cookie_domain import CookieDomainPolicy

class HttpCookieConverter:

    def __init__(
        self,
        domain_policy: CookieDomainPolicy,
    ) -> None:
        self._domain_policy = domain_policy

    def convert(
        self,
        cookie: StdlibCookie,
        *,
        request_url: str,
    ) -> Cookie:

        name = cookie.name
        value = cookie.value

        if not isinstance(value, str):
            raise ValueError(
                "HTTP cookie value is missing.",
            )

        domain = cookie.domain

        if not domain:
            raise ValueError(
                "HTTP cookie domain is missing.",
            )

        parsed_url = urlparse(request_url)
        request_host = parsed_url.hostname

        if not request_host:
            raise ValueError(
                f"HTTP cookie request URL has no host: "
                f"{request_url!r}",
            )

        resolution = (
            self._domain_policy.resolve_parsed_domain(
                request_host=request_host,
                domain=domain,
                host_only=not cookie.domain_specified,
            )
        )

        return Cookie(
            name=name,
            value=value,
            scope_domain=resolution.scope_domain,
            host_only=resolution.host_only,
            path=(
                cookie.path
                if cookie.path
                else "/"
            ),
            expires=self._expires(
                cookie.expires,
            ),
            secure=cookie.secure,
            http_only=(
                cookie.has_nonstandard_attr(
                    "HttpOnly",
                )
            ),
            same_site=self._same_site(
                cookie,
            ),
            partition_key=None,
        )

    def convert_many(
        self,
        cookies: Iterable[StdlibCookie],
        *,
        request_url: str,
    ) -> tuple[Cookie, ...]:

        return tuple(
            self.convert(
                cookie,
                request_url=request_url,
            )
            for cookie in cookies
        )

    @staticmethod
    def _same_site(
        cookie: StdlibCookie,
    ) -> SameSite | None:

        value = cookie.get_nonstandard_attr(
            "SameSite",
        )

        if not isinstance(value, str):
            return None

        value = value.lower()

        if value == "strict":
            return "strict"

        if value == "lax":
            return "lax"

        if value == "none":
            return "none"

        return None

    @staticmethod
    def _expires(
        value: int | None,
    ) -> datetime | None:

        if value is None:
            return None

        return datetime.fromtimestamp(
            value,
            tz=timezone.utc,
        )