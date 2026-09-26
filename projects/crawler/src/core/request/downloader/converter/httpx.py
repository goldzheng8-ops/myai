from core.request.downloader.converter.http import HttpCookieConverter
from core.request.middleware.cookie.model import Cookie
import httpx


class HttpxCookieConverter:

    @staticmethod
    def convert_many(
        cookies: httpx.Cookies,
    ) -> tuple[Cookie, ...]:

        return tuple(
            HttpCookieConverter.convert(
                cookie,
            )
            for cookie in cookies.jar
        )