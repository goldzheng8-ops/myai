from httpx import Response

from core.request.middleware.cookie.model import Cookie
from core.request.middleware.cookie.cookie_converter import HttpCookieConverter

class HttpxCookieExtractor:

    def __init__(
        self,
        converter: HttpCookieConverter,
    ) -> None:
        self._converter = converter

    def extract(
        self,
        response: Response,
    ) -> tuple[Cookie, ...]:

        cookies = response.cookies.jar

        framework_cookies = self._converter.convert_many(
            cookies,
            request_url=str(response.request.url),
        )

        return framework_cookies