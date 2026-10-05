from typing import Protocol

from core.request.middleware.cookie.model import Cookie
from core.request.middleware.session.model import Session





class BrowserCookieSink(Protocol):
    async def update(
        self,
        cookies: tuple[Cookie, ...],
    ) -> None:
        ...

class SessionCookieSink:
    """
    Adapts Framework Session CookieJar
    to BrowserCookieSink.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    async def update(
        self,
        cookies: tuple[Cookie, ...],
    ) -> None:

        self._session.cookies.update(
            cookies,
        )