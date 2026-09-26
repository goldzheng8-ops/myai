from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse

from core.request.middleware.cookie.model import Cookie, SameSite

class SetCookieParser:
    """
    Parse one HTTP Set-Cookie header directly into
    the framework Cookie model.
    """

    @staticmethod
    def parse(
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

        parts = SetCookieParser._split(
            header,
        )

        if not parts:
            return None

        name, value = (
            SetCookieParser._parse_pair(
                parts[0],
            )
        )

        if name is None or value is None:
            return None

        attributes = (
            SetCookieParser._parse_attributes(
                parts[1:],
            )
        )

        raw_domain = attributes.get(
            "domain",
        )

        if raw_domain is None:
            scope_domain = host.lower()
            host_only = True

        else:
            scope_domain = (
                SetCookieParser._normalize_domain(
                    raw_domain,
                )
            )

            if scope_domain is None:
                return None

            host_only = False

        raw_path = attributes.get(
            "path",
        )

        path = (
            raw_path
            if raw_path
            else SetCookieParser._default_path(
                request_path,
            )
        )

        max_age = (
            SetCookieParser._parse_max_age(
                attributes.get("max-age"),
            )
        )

        expires = (
            SetCookieParser._parse_expires(
                attributes.get("expires"),
            )
        )

        # Max-Age takes precedence over Expires.
        if max_age is not None:
            expires = (
                datetime.now(timezone.utc)
                + timedelta(
                    seconds=max_age,
                )
            )

        if not SetCookieParser._domain_matches_host(
            scope_domain,
            host,
        ):
            return None

        return Cookie(
            name=name,
            value=value,
            scope_domain=scope_domain,
            host_only=host_only,
            path=path,
            expires=expires,
            secure="secure" in attributes,
            http_only="httponly" in attributes,
            same_site=(
                SetCookieParser._parse_same_site(
                    attributes.get("samesite"),
                )
            ),
            partition_key=None,
        )

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

                result[name] = value

            else:

                name = part.strip().lower()

                if not name:
                    continue

                result[name] = ""

        return result

    @staticmethod
    def _normalize_domain(
        value: str,
    ) -> str | None:

        domain = value.strip().lower()

        if not domain:
            return None

        domain = domain.lstrip(".")

        if not domain:
            return None

        return domain

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

        if not value:
            return None

        try:
            return int(value)
        except ValueError:
            return None

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

    @staticmethod
    def _domain_matches_host(
        cookie_domain: str,
        host: str,
    ) -> bool:

        cookie_domain = (
            cookie_domain.lower()
        )

        host = host.lower()

        return (
            host == cookie_domain
            or host.endswith(
                f".{cookie_domain}",
            )
        )