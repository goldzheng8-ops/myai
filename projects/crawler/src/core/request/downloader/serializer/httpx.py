from http.cookiejar import Cookie as StdlibCookie
from typing import Iterable

from core.request.middleware.cookie.model import Cookie, SameSite
import httpx


class HttpxCookieSerializer:
    """
    Serialize framework Cookies into an httpx Cookies jar.

    The serializer preserves host-only/domain-cookie semantics by
    constructing stdlib http.cookiejar.Cookie objects directly.
    """

    @staticmethod
    def serialize(
        cookie: Cookie,
        *,
        jar: httpx.Cookies | None = None,
    ) -> httpx.Cookies:

        result = (
            jar
            if jar is not None
            else httpx.Cookies()
        )

        result.jar.set_cookie(
            HttpxCookieSerializer
            ._to_stdlib_cookie(
                cookie,
            )
        )

        return result

    @staticmethod
    def serialize_many(
        cookies: Iterable[Cookie],
        *,
        jar: httpx.Cookies | None = None,
    ) -> httpx.Cookies:

        result = (
            jar
            if jar is not None
            else httpx.Cookies()
        )

        for cookie in cookies:
            result.jar.set_cookie(
                HttpxCookieSerializer
                ._to_stdlib_cookie(
                    cookie,
                )
            )

        return result

    @staticmethod
    def _to_stdlib_cookie(
        cookie: Cookie,
    ) -> StdlibCookie:

        rest: dict[str, str] = {}

        if cookie.http_only:
            rest["HttpOnly"] = ""

        if cookie.same_site is not None:
            rest["SameSite"] = (
                HttpxCookieSerializer
                ._same_site(
                    cookie.same_site,
                )
            )

        return StdlibCookie(
            version=0,
            name=cookie.name,
            value=cookie.value,
            port=None,
            port_specified=False,
            domain=cookie.scope_domain,
            domain_specified=(
                not cookie.host_only
            ),
            domain_initial_dot=False,
            path=cookie.path,
            path_specified=True,
            secure=cookie.secure,
            expires=(
                int(cookie.expires.timestamp())
                if cookie.expires is not None
                else None
            ),
            discard=(
                cookie.expires is None
            ),
            comment=None,
            comment_url=None,
            rest=rest,
            rfc2109=False,
        )

    @staticmethod
    def _same_site(
        value: SameSite,
    ) -> str:

        if value == "strict":
            return "Strict"

        if value == "lax":
            return "Lax"

        if value == "none":
            return "None"

        raise ValueError(
            f"Unsupported SameSite value: {value!r}",
        )