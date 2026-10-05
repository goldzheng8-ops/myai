from core.request.middleware.cookie.cookie_parser import SetCookieParser
from core.request.middleware.cookie.model import Cookie
from playwright.async_api import Response


class PlaywrightCookieExtractor:

    def __init__(
        self,
        set_cookie_parser: SetCookieParser,
    ) -> None:
        self._set_cookie_parser = set_cookie_parser

    async def extract(
        self,
        response: Response,
    ) -> tuple[Cookie, ...]:

        headers = await response.header_values(
            "set-cookie",
        )

        if not headers:
            return ()

        cookies = self._set_cookie_parser.parse_many(
            headers,
            url=response.url,
        )

        return cookies