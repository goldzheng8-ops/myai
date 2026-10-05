from __future__ import annotations
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable
from urllib.parse import urlparse

from core.request.middleware.cookie.model import Cookie, SameSite
from core.request.middleware.cookie.policy.cookie_domain import CookieDomainPolicy
from core.request.middleware.cookie.policy.exception import InvalidCookieDomain


class SetCookieParser:

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
        request_host = parsed_url.hostname

        if not request_host:
            return None

        request_path = parsed_url.path or "/"

        parts = self._split(header)

        if not parts:
            return None

        name, value = self._parse_pair(
            parts[0],
        )

        if name is None or value is None:
            return None

        if not self._valid_cookie_name(name):
            return None

        attributes = self._parse_attributes(
            parts[1:],
        )

        domain_attribute = attributes.get(
            "domain",
        )

        try:
            domain = self._domain_policy.resolve_set_cookie_domain(
                request_host=request_host,
                domain_attribute=domain_attribute,
            )
        except InvalidCookieDomain:
            return None

        path = self._resolve_path(
            path_attribute=attributes.get("path"),
            request_path=request_path,
        )

        max_age = self._parse_max_age(
            attributes.get("max-age"),
        )

        expires = self._parse_expires(
            attributes.get("expires"),
        )

        # Max-Age takes precedence over Expires.
        if max_age is not None:
            expires = (
                datetime.now(timezone.utc)
                + timedelta(seconds=max_age)
            )

        return Cookie(
            name=name,
            value=value,
            scope_domain=domain.scope_domain,
            host_only=domain.host_only,
            path=path,
            expires=expires,
            secure="secure" in attributes,
            http_only="httponly" in attributes,
            same_site=self._parse_same_site(
                attributes.get("samesite"),
            ),
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

            if cookie is not None:
                result.append(cookie)

        return tuple(result)

    @staticmethod
    def _split(
        header: str,
    ) -> list[str]:

        return [
            part.strip()
            for part in header.split(";")
            if part.strip()
        ]

    @staticmethod
    def _parse_pair(
        pair: str,
    ) -> tuple[str | None, str | None]:

        if "=" not in pair:
            return None, None

        name, value = pair.split(
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
        parts: Iterable[str],
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

                if name:
                    result[name] = value

            else:
                name = part.strip().lower()

                if name:
                    result[name] = ""

        return result

    @staticmethod
    def _resolve_path(
        *,
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

    @staticmethod
    def _parse_max_age(
        value: str | None,
    ) -> int | None:

        if value is None:
            return None

        try:
            return int(value.strip())
        except ValueError:
            return None

    @staticmethod
    def _parse_expires(
        value: str | None,
    ) -> datetime | None:

        if value is None:
            return None

        try:
            result = parsedate_to_datetime(
                value,
            )
        except (TypeError, ValueError, OverflowError):
            return None

        if result.tzinfo is None:
            result = result.replace(
                tzinfo=timezone.utc,
            )

        return result.astimezone(
            timezone.utc,
        )

    @staticmethod
    def _parse_same_site(
        value: str | None,
    ) -> SameSite | None:

        if value is None:
            return None

        value = value.strip().lower()

        if value == "strict":
            return "strict"

        if value == "lax":
            return "lax"

        if value == "none":
            return "none"

        return None

    @staticmethod
    def _valid_cookie_name(
        name: str,
    ) -> bool:

        return all(
            (
                "A" <= char <= "Z"
                or "a" <= char <= "z"
                or "0" <= char <= "9"
                or char in "!#$%&'*+-.^_`|~"
            )
            for char in name
        )