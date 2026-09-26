from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from http.cookiejar import Cookie as StdlibCookie
from http.cookies import Morsel, SimpleCookie
from urllib.parse import urlparse

from core.request.downloader.converter.http import HttpCookieConverter
from core.request.middleware.cookie.model import Cookie
from playwright.async_api import Response


class PlaywrightCookieExtractor:

    @staticmethod
    async def extract(
        response: Response,
    ) -> tuple[Cookie, ...]:

        headers = await response.header_values(
            "set-cookie",
        )

        if not headers:
            return ()

        url = response.url

        result: list[Cookie] = []

        for header in headers:

            cookies = (
                PlaywrightCookieExtractor
                ._parse_header(
                    header,
                    url,
                )
            )

            result.extend(
                HttpCookieConverter.convert_many(
                    cookies,
                )
            )

        return tuple(result)

    @staticmethod
    def _parse_header(
        header: str,
        url: str,
    ) -> tuple[StdlibCookie, ...]:

        parsed = SimpleCookie()

        try:
            parsed.load(header)
        except Exception:
            return ()

        if not parsed:
            return ()

        parsed_url = urlparse(url)

        host = parsed_url.hostname

        if not host:
            return ()

        request_path = (
            parsed_url.path
            or "/"
        )

        return tuple(
            PlaywrightCookieExtractor
            ._to_stdlib_cookie(
                morsel,
                host=host,
                request_path=request_path,
            )
            for morsel in parsed.values()
        )

    @staticmethod
    def _to_stdlib_cookie(
        morsel: Morsel[str],
        *,
        host: str,
        request_path: str,
    ) -> StdlibCookie:

        raw_domain = morsel["domain"]

        domain_specified = bool(
            raw_domain,
        )

        domain = (
            raw_domain.lstrip(".").lower()
            if raw_domain
            else host.lower()
        )

        raw_path = morsel["path"]

        path = (
            raw_path
            if raw_path
            else PlaywrightCookieExtractor
            ._default_path(
                request_path,
            )
        )

        expires = (
            PlaywrightCookieExtractor
            ._parse_expires(
                morsel["expires"],
            )
        )

        max_age = (
            PlaywrightCookieExtractor
            ._parse_max_age(
                morsel["max-age"],
            )
        )

        if max_age is not None:
            expires = int(
                datetime.now(
                    timezone.utc,
                ).timestamp()
                + max_age,
            )

        rest: dict[str, str] = {}

        if morsel["httponly"]:
            rest["HttpOnly"] = ""

        if morsel["samesite"]:
            rest["SameSite"] = (
                morsel["samesite"]
            )

        return StdlibCookie(
            version=0,
            name=morsel.key,
            value=morsel.value,
            port=None,
            port_specified=False,
            domain=domain,
            domain_specified=domain_specified,
            domain_initial_dot=(
                raw_domain.startswith(".")
                if raw_domain
                else False
            ),
            path=path,
            path_specified=bool(
                raw_path,
            ),
            secure=bool(
                morsel["secure"],
            ),
            expires=expires,
            discard=expires is None,
            comment=None,
            comment_url=None,
            rest=rest,
            rfc2109=False,
        )

    @staticmethod
    def _parse_expires(
        value: str,
    ) -> int | None:

        if not value:
            return None

        try:
            parsed = parsedate_to_datetime(
                value,
            )
        except (TypeError, ValueError):
            return None

        if parsed.tzinfo is None:
            parsed = parsed.replace(
                tzinfo=timezone.utc,
            )

        return int(
            parsed.timestamp(),
        )

    @staticmethod
    def _parse_max_age(
        value: str,
    ) -> int | None:

        if not value:
            return None

        try:
            return int(value)
        except ValueError:
            return None

    @staticmethod
    def _default_path(
        request_path: str,
    ) -> str:

        if not request_path.startswith("/"):
            return "/"

        if request_path.count("/") <= 1:
            return "/"

        directory = request_path.rsplit(
            "/",
            1,
        )[0]

        return directory or "/"