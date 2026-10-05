from collections.abc import Sequence
from typing import Iterable, Literal, Optional, TypedDict

from core.request.middleware.cookie.model import Cookie, SameSite

class SetCookieParam(TypedDict, total=False):
    name: str
    value: str
    url: Optional[str]
    domain: Optional[str]
    path: Optional[str]
    expires: Optional[float]
    httpOnly: Optional[bool]
    secure: Optional[bool]
    sameSite: Optional[Literal["Lax", "None", "Strict"]]
    partitionKey: Optional[str]

sameSite=Literal['Lax', 'None', 'Strict']
class PlaywrightCookieSerializer:

    @staticmethod
    def serialize(
        cookie: Cookie,
        *,
        url: str | None = None,
    ) -> SetCookieParam:

        result: SetCookieParam = {
            "name": cookie.name,
            "value": cookie.value,
            "path": cookie.path,
            "secure": cookie.secure,
            "httpOnly": cookie.http_only,
        }

        if cookie.host_only:

            if url is None:
                raise ValueError(
                    "A URL is required to serialize "
                    "a host-only cookie for Playwright.",
                )

            result["url"] = url

        else:

            result["domain"] = (
                "."
                + cookie.scope_domain
            )

        if cookie.expires is not None:
            result["expires"] = (
                cookie.expires.timestamp()
            )

        if cookie.same_site is not None:
            result["sameSite"] = (
                PlaywrightCookieSerializer
                ._same_site(
                    cookie.same_site,
                )
            )

        if cookie.partition_key is not None:
            result["partitionKey"] = (
                cookie.partition_key
            )

        return result

    @staticmethod
    def _same_site(
        value: SameSite,
    ) -> sameSite:

        if value == "strict":
            return "Strict"

        if value == "lax":
            return "Lax"

        if value == "none":
            return "None"

        raise ValueError(
            f"Unsupported SameSite value: {value!r}",
        )

    @staticmethod
    def serialize_many(
        cookies: Iterable[Cookie],
        *,
        url: str | None = None,
    ) -> Sequence[SetCookieParam]:

        return tuple(
            PlaywrightCookieSerializer.serialize(
                cookie,
                url=url,
            )
            for cookie in cookies
        )