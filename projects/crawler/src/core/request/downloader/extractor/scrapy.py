from scrapy.http import Response
from scrapy.http.cookies import CookieJar as ScrapyCookieJar

from core.request.middleware.cookie.model import Cookie
from core.request.middleware.cookie.cookie_converter import HttpCookieConverter



class ScrapyCookieExtractor:

    def __init__(
        self,
        converter: HttpCookieConverter,
    ) -> None:
        self._converter = converter

    def extract(
        self,
        response: Response,
    ) -> tuple[Cookie, ...]:

        request = response.request

        if request is None:
            return ()

        request_url = request.url

        jar = ScrapyCookieJar()

        cookies = jar.make_cookies(
            response,
            request,
        )

        return self._converter.convert_many(
            cookies,
            request_url=request_url,
        )