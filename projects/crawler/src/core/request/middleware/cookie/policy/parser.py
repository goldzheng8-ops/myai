from __future__ import annotations
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable
from urllib.parse import urlparse

from core.request.middleware.cookie.model import Cookie, SameSite
from core.request.middleware.cookie.policy.cookie_domain import CookieDomainPolicy
from core.request.middleware.cookie.policy.exception import InvalidCookieDomain


class SetCookieParser:
    """
    Parse HTTP Set-Cookie headers directly into
    framework Cookie objects.
    """

    def __init__(
        self,
        domain_policy: CookieDomainPolicy,
    ) -> None:

        self._domain_policy = domain_policy

    def parse(
        self,
        header: str,
        *,
        url: str,
    ) -> Cookie | None:

        header = header.strip()

        if not header:
            return None

        parsed_url = urlparse(url)

        host = parsed_url.hostname

        if not host:
            return None

        request_path = (
            parsed_url.path
            or "/"
        )

        parts = self._split(
            header,
        )

        if not parts:
            return None

        name, value = self._parse_pair(
            parts[0],
        )

        if name is None or value is None:
            return None

        if not self._valid_cookie_name(
            name,
        ):
            return None

        attributes = (
            self._parse_attributes(
                parts[1:],
            )
        )

        # -----------------------------------------------------
        # Domain
        # -----------------------------------------------------

        try:
            domain = self._domain_policy.resolve(
                request_host=host,
                domain_attribute=attributes.get(
                    "domain",
                ),
            )
        except InvalidCookieDomain:
            return None

        # -----------------------------------------------------
        # Path
        # -----------------------------------------------------

        path = self._resolve_path(
            attributes.get("path"),
            request_path,
        )

        # -----------------------------------------------------
        # Expiration
        # -----------------------------------------------------

        expires = self._parse_expires(
            attributes.get("expires"),
        )

        max_age = self._parse_max_age(
            attributes.get("max-age"),
        )

        if max_age is not None:

            expires = (
                datetime.now(timezone.utc)
                + timedelta(
                    seconds=max_age,
                )
            )

        # -----------------------------------------------------
        # SameSite
        # -----------------------------------------------------

        same_site = self._parse_same_site(
            attributes.get("samesite"),
        )

        # -----------------------------------------------------
        # Cookie
        # -----------------------------------------------------

        return Cookie(
            name=name,
            value=value,
            scope_domain=domain.scope_domain,
            host_only=domain.host_only,
            path=path,
            expires=expires,
            secure="secure" in attributes,
            http_only="httponly" in attributes,
            same_site=same_site,
            partition_key=None,
        )

    def parse_many(
        self,
        headers: Iterable[str],
        *,
        url: str,
    ) -> tuple[Cookie, ...]:

        result: list[Cookie] = []

        for header in headers:

            cookie = self.parse(
                header,
                url=url,
            )

            if cookie is None:
                continue

            result.append(cookie)

        return tuple(result)

    # ---------------------------------------------------------
    # cookie pair
    # ---------------------------------------------------------

    @staticmethod
    def _split(
        header: str,
    ) -> tuple[str, ...]:

        return tuple(
            part.strip()
            for part in header.split(";")
            if part.strip()
        )

    @staticmethod
    def _parse_pair(
        part: str,
    ) -> tuple[str | None, str | None]:

        if "=" not in part:
            return None, None

        name, value = part.split(
            "=",
            1,
        )

        name = name.strip()
        value = value.strip()

        if not name:
            return None, None

        return name, value

    @staticmethod
    def _parse_attributes(
        parts: tuple[str, ...],
    ) -> dict[str, str]:

        result: dict[str, str] = {}

        for part in parts:

            if "=" in part:

                name, value = part.split(
                    "=",
                    1,
                )

                name = name.strip().lower()
                value = value.strip()

                if not name:
                    continue

                # Last attribute wins.
                result[name] = value

            else:

                name = part.strip().lower()

                if not name:
                    continue

                result[name] = ""

        return result

    # ---------------------------------------------------------
    # cookie name
    # ---------------------------------------------------------

    @staticmethod
    def _valid_cookie_name(
        name: str,
    ) -> bool:

        # RFC 6265 cookie-name is a token.
        #
        # RFC 7230 token characters are:
        # !#$%&'*+-.^_`|~ plus alphanumeric.
        #
        return all(
            (
                "A" <= char <= "Z"
                or "a" <= char <= "z"
                or "0" <= char <= "9"
                or char in "!#$%&'*+-.^_`|~"
            )
            for char in name
        )

    # ---------------------------------------------------------
    # path
    # ---------------------------------------------------------

    @staticmethod
    def _resolve_path(
        path_attribute: str | None,
        request_path: str,
    ) -> str:

        if (
            path_attribute is None
            or not path_attribute.startswith("/")
        ):
            return SetCookieParser._default_path(
                request_path,
            )

        return path_attribute

    @staticmethod
    def _default_path(
        request_path: str,
    ) -> str:

        if not request_path.startswith("/"):
            return "/"

        if request_path == "/":
            return "/"

        index = request_path.rfind("/")

        if index <= 0:
            return "/"

        return request_path[:index]

    # ---------------------------------------------------------
    # expiration
    # ---------------------------------------------------------

    @staticmethod
    def _parse_expires(
        value: str | None,
    ) -> datetime | None:

        if not value:
            return None

        try:
            parsed = parsedate_to_datetime(
                value,
            )
        except (
            TypeError,
            ValueError,
        ):
            return None

        if parsed.tzinfo is None:
            parsed = parsed.replace(
                tzinfo=timezone.utc,
            )

        return parsed.astimezone(
            timezone.utc,
        )

    @staticmethod
    def _parse_max_age(
        value: str | None,
    ) -> int | None:

        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        try:
            return int(value)
        except ValueError:
            return None

    # ---------------------------------------------------------
    # SameSite
    # ---------------------------------------------------------

    @staticmethod
    def _parse_same_site(
        value: str | None,
    ) -> SameSite | None:

        if not value:
            return None

        value = value.strip().lower()

        if value == "strict":
            return "strict"

        if value == "lax":
            return "lax"

        if value == "none":
            return "none"

        return None