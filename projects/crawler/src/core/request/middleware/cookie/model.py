from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from ipaddress import ip_address
from typing import Iterable, Iterator
from urllib.parse import urlparse
from typing import Literal


SameSite = Literal[
    "lax",
    "strict",
    "none",
]

@dataclass(frozen=True, slots=True, kw_only=True)
class Cookie:

    name: str
    value: str

    scope_domain: str
    host_only: bool

    path: str = "/"

    expires: datetime | None = None

    secure: bool = False
    http_only: bool = False

    same_site: SameSite | None = None

    partition_key: str | None = None


class CookieJar:

    _cookies: dict[
        tuple[str, str, str],
        Cookie,
    ]

    def __init__(self) -> None:
        self._cookies = {}

    # ---------------------------------------------------------
    # mutation
    # ---------------------------------------------------------

    def set(
        self,
        cookie: Cookie,
    ) -> None:

        key = self._key(cookie)

        if self._is_expired(cookie):
            self._cookies.pop(
                key,
                None,
            )
            return

        self._cookies[key] = cookie

    def update(
        self,
        cookies: Iterable[Cookie],
    ) -> None:

        for cookie in cookies:
            self.set(cookie)

    def remove(
        self,
        cookie: Cookie,
    ) -> None:

        self._cookies.pop(
            self._key(cookie),
            None,
        )

    def clear(self) -> None:
        self._cookies.clear()

    # ---------------------------------------------------------
    # request
    # ---------------------------------------------------------

    def get_for_url(
        self,
        url: str,
    ) -> tuple[Cookie, ...]:

        parsed = urlparse(url)

        host = parsed.hostname

        if not host:
            return ()

        request_path = (
            parsed.path
            or "/"
        )

        secure = (
            parsed.scheme.lower()
            == "https"
        )

        now = datetime.now(
            timezone.utc,
        )

        matched: list[Cookie] = []

        expired_keys: list[
            tuple[str, str, str]
        ] = []

        for key, cookie in self._cookies.items():

            if self._is_expired(
                cookie,
                now,
            ):
                expired_keys.append(key)
                continue

            if not self._domain_matches(
                cookie,
                host,
            ):
                continue

            if not self._path_matches(
                cookie.path,
                request_path,
            ):
                continue

            if cookie.secure and not secure:
                continue

            matched.append(cookie)

        # RFC 6265 recommends evicting expired
        # cookies when encountered.
        for key in expired_keys:
            self._cookies.pop(
                key,
                None,
            )

        # Longer paths first.
        matched.sort(
            key=lambda cookie: len(
                cookie.path,
            ),
            reverse=True,
        )

        return tuple(matched)

    # ---------------------------------------------------------
    # inspection
    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[Cookie]:

        return iter(
            self._cookies.values(),
        )

    def __len__(self) -> int:
        return len(self._cookies)

    # ---------------------------------------------------------
    # identity
    # ---------------------------------------------------------

    @staticmethod
    def _key(
        cookie: Cookie,
    ) -> tuple[str, str, str]:

        return (
            cookie.scope_domain,
            cookie.path,
            cookie.name,
        )

    # ---------------------------------------------------------
    # expiration
    # ---------------------------------------------------------

    @staticmethod
    def _is_expired(
        cookie: Cookie,
        now: datetime | None = None,
    ) -> bool:

        expires = cookie.expires

        if expires is None:
            return False

        if now is None:
            now = datetime.now(
                timezone.utc,
            )

        if expires.tzinfo is None:
            expires = expires.replace(
                tzinfo=timezone.utc,
            )

        return expires <= now

    # ---------------------------------------------------------
    # domain matching
    # ---------------------------------------------------------

    @staticmethod
    def _domain_matches(
        cookie: Cookie,
        host: str,
    ) -> bool:

        cookie_domain = (
            cookie.scope_domain.lower()
        )

        host = host.lower()

        if cookie.host_only:
            return host == cookie_domain

        return CookieJar._domain_match(
            host,
            cookie_domain,
        )

    @staticmethod
    def _domain_match(
        host: str,
        domain: str,
    ) -> bool:

        if host == domain:
            return True

        if CookieJar._is_ip_address(host):
            return False

        if not host.endswith(domain):
            return False

        index = len(host) - len(domain) - 1

        return (
            index >= 0
            and host[index] == "."
        )

    @staticmethod
    def _is_ip_address(
        host: str,
    ) -> bool:

        try:
            ip_address(host)
        except ValueError:
            return False

        return True

    # ---------------------------------------------------------
    # path matching
    # ---------------------------------------------------------

    @staticmethod
    def _path_matches(
        cookie_path: str,
        request_path: str,
    ) -> bool:

        if not cookie_path:
            cookie_path = "/"

        if not request_path:
            request_path = "/"

        # RFC 6265 section 5.1.4:
        #
        # 1. identical paths
        if cookie_path == request_path:
            return True

        # Cookie path must be a prefix.
        if not request_path.startswith(
            cookie_path,
        ):
            return False

        # 2. Cookie path ends with "/"
        if cookie_path.endswith("/"):
            return True

        # 3. The first character of request_path
        #    after cookie_path must be "/".
        if len(request_path) <= len(cookie_path):
            return False

        return (
            request_path[
                len(cookie_path)
            ]
            == "/"
        )