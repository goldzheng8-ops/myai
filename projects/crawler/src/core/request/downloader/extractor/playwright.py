from core.request.downloader.extractor.parser import SetCookieParser
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

        result: list[Cookie] = []

        for header in headers:

            cookie = (
                SetCookieParser.parse(
                    header,
                    url=response.url,
                )
            )

            if cookie is None:
                continue

            result.append(cookie)

        return tuple(result)