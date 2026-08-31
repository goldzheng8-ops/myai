from dataclasses import dataclass
from urllib.parse import quote, urlsplit, urlunsplit


@dataclass(frozen=True, slots=True)
class ProxyConfig:
    """
    Proxy configuration used by a request.
    """

    url: str

    username: str | None = None

    password: str | None = None

    def as_url(self) -> str:
        """
        Return the proxy URL with optional authentication.
        """

        if self.username is None:
            return self.url

        parts = urlsplit(self.url)

        username = quote(
            self.username,
            safe="",
        )

        password = (
            quote(
                self.password,
                safe="",
            )
            if self.password is not None
            else ""
        )

        host = parts.hostname or ""

        if parts.port is not None:
            host = f"{host}:{parts.port}"

        netloc = f"{username}:{password}@{host}"

        return urlunsplit(
            (
                parts.scheme,
                netloc,
                parts.path,
                parts.query,
                parts.fragment,
            )
        )