from dataclasses import dataclass
from urllib.parse import urlparse
from typing import Literal
from datetime import datetime, timezone
from collections.abc import Iterable, Iterator

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

        path = parsed.path or "/"

        secure = (
            parsed.scheme.lower()
            == "https"
        )

        now = datetime.now(
            timezone.utc,
        )

        matched: list[Cookie] = []

        for cookie in self._cookies.values():

            if self._is_expired(
                cookie,
                now,
            ):
                continue

            if not self._domain_matches(
                cookie,
                host,
            ):
                continue

            if not self._path_matches(
                cookie.path,
                path,
            ):
                continue

            if cookie.secure and not secure:
                continue

            matched.append(cookie)

        # RFC cookie ordering:
        # longer paths first.
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
    # helpers
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

    @staticmethod
    def _is_expired(
        cookie: Cookie,
        now: datetime | None = None,
    ) -> bool:

        if cookie.expires is None:
            return False

        if now is None:
            now = datetime.now(
                timezone.utc,
            )

        return cookie.expires <= now

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

        return (
            host == cookie_domain
            or host.endswith(
                f".{cookie_domain}",
            )
        )

    @staticmethod
    def _path_matches(
        cookie_path: str,
        request_path: str,
    ) -> bool:

        if not cookie_path:
            cookie_path = "/"

        if not request_path:
            request_path = "/"

        if cookie_path == "/":
            return True

        if request_path == cookie_path:
            return True

        if not request_path.startswith(
            cookie_path,
        ):
            return False

        return (
            cookie_path.endswith("/")
            or request_path[
                len(cookie_path):
            ].startswith("/")
        )