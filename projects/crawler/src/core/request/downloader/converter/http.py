from datetime import datetime, timezone
from http.cookiejar import Cookie as StdlibCookie
from typing import Iterable

from core.request.middleware.cookie.model import Cookie, SameSite

class HttpCookieConverter:

    @staticmethod
    def convert(
        cookie: StdlibCookie,
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

        return Cookie(
            name=name,
            value=value,
            scope_domain=(
                domain.lstrip(".")
            ),
            host_only=(
                not cookie.domain_specified
            ),
            path=(
                cookie.path
                if cookie.path
                else "/"
            ),
            expires=(
                HttpCookieConverter._expires(
                    cookie.expires,
                )
            ),
            secure=cookie.secure,
            http_only=(
                cookie.has_nonstandard_attr(
                    "HttpOnly",
                )
            ),
            same_site=(
                HttpCookieConverter._same_site(
                    cookie,
                )
            ),
        )

    @staticmethod
    def convert_many(
        cookies: Iterable[StdlibCookie],
    ) -> tuple[Cookie, ...]:

        return tuple(
            HttpCookieConverter.convert(
                cookie,
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