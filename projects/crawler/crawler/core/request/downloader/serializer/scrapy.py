from typing import Iterable

from core.request.middleware.cookie.model import Cookie


class ScrapyCookieSerializer:

    @staticmethod
    def serialize(
        cookies: Iterable[Cookie],
    ) -> str:

        return "; ".join(
            (
                f"{cookie.name}="
                f"{cookie.value}"
            )
            for cookie in cookies
        )