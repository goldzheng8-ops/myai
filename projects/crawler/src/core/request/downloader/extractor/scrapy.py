from scrapy.http import Response
from scrapy.http.cookies import CookieJar as ScrapyCookieJar

from core.request.middleware.cookie.model import Cookie
from core.request.downloader.converter.http import HttpCookieConverter



class ScrapyCookieExtractor:
    """
    Extract framework cookies from a Scrapy response.

    This extractor does not own cookie state.
    It uses a temporary Scrapy CookieJar only
    for parsing Set-Cookie response headers.
    """

    @staticmethod
    def extract(
        response: Response,
    ) -> tuple[Cookie, ...]:

        request = response.request

        if request is None:
            return ()

        jar = ScrapyCookieJar()

        cookies = jar.make_cookies(
            response,
            request,
        )

        return HttpCookieConverter.convert_many(
            cookies,
        )

